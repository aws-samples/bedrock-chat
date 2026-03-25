# Bedrock Chat — Claude Code Session Memory

## Project Overview
AWS-native chatbot using Amazon Bedrock. Deployed via CDK + CodeBuild from this repo (DPenniket/bedrock-chat, branch `v3`).
- **Frontend**: React/Vite, hosted on S3/CloudFront
- **Backend**: Lambda (Python 3.13), API Gateway (WebSocket + REST)
- **Repo**: https://github.com/DPenniket/bedrock-chat

## Deploy Command (run from CloudShell)
```bash
./bin.sh --disable-self-register --bedrock-region ap-southeast-2 --repo-url https://github.com/DPenniket/bedrock-chat.git --version v3
```
- This triggers a CloudFormation stack (`CodeBuildForDeploy`) which starts a CodeBuild project
- CodeBuild does: `git clone --branch v3 https://github.com/DPenniket/bedrock-chat.git` then `npx cdk deploy --require-approval never --all`
- Deploy is to `ap-southeast-2` (Sydney)

---

## The Problem Being Solved
**Symptom**: Uploading a ~4MB PDF to the chat causes "An error occurred while responding." in the UI. Browser console shows `{"message": "Internal server error", "connectionId":"...", "requestId":"..."}` received via WebSocket.

**Root cause**: API Gateway WebSocket **replaces the Lambda response body with its own error format** whenever Lambda returns a non-2xx HTTP status code. The `{"message": "Internal server error", ...}` format is API Gateway's own message, NOT our Lambda's. The client's `ws.onmessage` handler JSON-parses this, sees no `data.status` field, and calls `reject()` with the generic error without ever setting `errorDetail` in Zustand — so the UI always shows the generic message with no detail about what actually went wrong.

---

## Architecture: WebSocket Large Message Chunking

The WebSocket API Gateway has a hard 32KB-per-message limit. For large payloads (e.g. messages embedding PDF content), a chunking protocol was built:

### Frontend (`frontend/src/hooks/usePostMessageStreaming.ts`)
```
CHUNK_SIZE = 32 * 1024  // 32KB characters
payloadString = JSON.stringify({ ...chatInput, token })
```
1. **START**: Client sends `{step: "START", token}` → waits for `"Session started."`
2. **BODY**: Client sends ALL chunks simultaneously: `{step: "BODY", index, part: chunk}` for each chunk — waits for each `"Message part received."` ack
3. **END**: After all acks received (`receivedCount === chunkedPayloads.length`), sends `{step: "END", token}`

**Important**: All BODY chunks are sent at once (in parallel), creating many concurrent Lambda invocations (e.g. a 4.1MB PDF → ~172 chunks → ~172 concurrent Lambda calls).

### Backend (`backend/app/websocket.py`)
- **START**: Verifies token, stores `{"user_id": ...}` in S3 at `ws-chunks/{connection_id}/session.json`
- **BODY**: Stores each chunk to S3 at `ws-chunks/{connection_id}/{index:010d}`
- **END**: Reads session from S3, lists + reads all chunks in parallel (ThreadPoolExecutor, max 20 workers), assembles full message, calls `process_chat_input()` → Bedrock

### S3 Bucket
Environment variable: `LARGE_PAYLOAD_SUPPORT_BUCKET` → maps to `largePayloadSupportBucket` in CDK (`websocket.ts`)

---

## Code Changes Made (All in `backend/app/websocket.py`)

### What was fixed (merged to v3)
All of these changes ensure Lambda **always returns `statusCode: 200`** — the actual error detail is sent to the client exclusively via `post_to_connection` (which API Gateway never intercepts):

1. **START step invalid token** — was returning `statusCode: 403`, now calls `notificator.notify(ERROR)` + returns 200
2. **Outer `handler()` except** — was returning `statusCode: 500`, now calls `notificator.notify(ERROR)` + returns 200
3. **`process_chat_input` RecordNotFoundError** — was returning `statusCode: 400/404`, now returns 200
4. **`process_chat_input` generic except** — was returning `statusCode: 500`, now returns 200
5. **`json.loads(event["body"])`** — was OUTSIDE the try block; if body is None/malformed, Lambda runtime sets `X-Amz-Function-Error` header which API Gateway also converts to "Internal server error". Moved INSIDE the try block.

Current state of the v3 branch: **all the above fixes are in place** (PRs #49 and #50 merged).

---

## The Unresolved Problem

Despite the above fixes being deployed, the user reports **no change** in behaviour — the error still appears with no actionable reason shown to the user. Possible causes that are still undiagnosed:

### Hypothesis 1: Lambda concurrency throttling (most likely)
With ~172 BODY chunks sent at once → ~172 concurrent Lambda invocations. If Lambda is throttled (account-level concurrency limit, reserved concurrency, or burst limit), the Lambda service returns a `429 TooManyRequests` to API Gateway **before Lambda even runs**. Our code fixes can't help — Lambda never executes. API Gateway converts the throttle to `{"message": "Internal server error", ...}`.

- **ap-southeast-2 burst limit**: 500 concurrent invocations
- **Default account limit**: 1000 concurrent invocations
- Check: Lambda console → Concurrency metrics

### Hypothesis 2: Deployment not actually applying changes
User reports "zero impact" from all changes. Possible causes:
- The CDK deploy might be failing silently on the Lambda stack while succeeding on others
- Lambda asset hash might not be recomputed correctly
- User might be accessing a different endpoint/environment

### Hypothesis 3: Different root cause than expected
The `GET .../bot?kind=private 503 (Service Unavailable)` REST API error also appears in the console — not directly related to WebSocket but may indicate broader infrastructure issues.

---

## How to Verify the Deployment Is Working

**Step 1: Confirm Lambda code is updated**
- AWS Console → Lambda → search for `WebSocket` handler → Code tab → open `app/websocket.py`
- Look for `json.loads(event["body"])` being INSIDE the `try:` block (our most recent fix)
- If it's still before the `notification_thread = Thread(...)` line, the new code wasn't deployed

**Step 2: Check CloudWatch logs for the failing Lambda invocation**
- CloudWatch → Log groups → find the WebSocket Lambda log group
- Filter for the time of a failed PDF upload
- Look for `"Received event:"` log entries for BODY step invocations
- If NO logs appear for some invocations → those were throttled (never ran)
- If logs appear with `"Operation failed:"` → our code caught the exception; the reason is logged there

**Step 3: Check Lambda concurrency**
- AWS Console → Lambda → the WebSocket handler → Monitor tab → Concurrency graph
- Look for throttles during a PDF upload attempt

**Step 4: Add a version marker (quick smoke test)**
To confirm a new deployment actually updated Lambda, temporarily add a distinctive log line and redeploy:
```python
logger.info("DEPLOYMENT_VERSION_v2_CHECK")  # add near top of handler()
```
Then upload anything and check CloudWatch — if you don't see that string, the deploy didn't update the Lambda.

---

## Frontend Error Flow (for reference)
```
ws.onmessage receives {"message": "Internal server error", ...}
→ JSON.parse succeeds
→ data.status is undefined → goes to else branch
→ ws.close(); throw new Error('error.predict.invalidResponse')
→ caught by outer catch → reject('error.predict.general')
→ errorDetail is NEVER SET (only set in case PostStreamingStatus.ERROR:)
→ UI shows generic "An error occurred while responding."
```
When our fixes work correctly:
```
Lambda catches error → notificator.notify({"status": "ERROR", "reason": "actual reason"})
→ post_to_connection delivers this to client
→ client receives it → data.status === "ERROR" → set({ errorDetail: data.reason })
→ UI shows actual reason
```
But for throttled invocations (Lambda never runs), `notificator.notify` is never called → client still gets API Gateway's "Internal server error" → `errorDetail` never set.

---

## Lambda Configuration (CDK — `cdk/lib/constructs/websocket.ts`)
- **Runtime**: Python 3.13
- **Memory**: 512 MB
- **Timeout**: 15 minutes
- **SnapStart**: Conditional (`enableLambdaSnapStart` in `cdk/cdk.json`, default `false`)
- **Concurrency**: No reserved concurrency set
- **API Gateway integration**: Uses `handler.currentVersion` (published Lambda version)

---

## Next Steps (Priority Order)

1. **Redeploy with latest v3 code** (both PRs #49 and #50 are now merged to v3)
2. **After deploy, verify Lambda code** via console (Step 1 above)
3. **Test upload and check CloudWatch** — does `"Operation failed:"` appear? Or no logs at all (throttle)?
4. **If throttling**: Fix is in the frontend — rate-limit BODY chunk sending (e.g. send in batches of 5 with a small delay, or send one at a time)
5. **If different error**: The actual error reason will now appear in CloudWatch logs and (if `post_to_connection` succeeds) in the frontend error panel

## File Locations
- Backend WebSocket handler: `backend/app/websocket.py`
- Frontend streaming hook: `frontend/src/hooks/usePostMessageStreaming.ts`
- CDK WebSocket construct: `cdk/lib/constructs/websocket.ts`
- Deploy script: `bin.sh` + `deploy.yml`
- Dev branch: `claude/increase-upload-limit-5kdsn`
