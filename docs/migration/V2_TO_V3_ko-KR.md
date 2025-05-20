# 마이그레이션 가이드 (v2에서 v3로)

## TL;DR

- V3에서는 세분화된 권한 제어 및 봇 스토어 기능을 도입하며, DynamoDB 스키마 변경이 필요합니다
- **마이그레이션 전에 DynamoDB ConversationTable을 백업하세요**
- 저장소 URL을 `bedrock-claude-chat`에서 `bedrock-chat`으로 업데이트하세요
- 마이그레이션 스크립트를 실행하여 데이터를 새 스키마로 변환하세요
- 모든 봇과 대화는 새 권한 모델로 보존됩니다
- **중요: 마이그레이션 프로세스 동안 마이그레이션이 완료될 때까지 모든 사용자에게 애플리케이션을 사용할 수 없게 됩니다. 이 프로세스는 데이터 양과 개발 환경의 성능에 따라 일반적으로 약 60분이 소요됩니다.**
- **중요: 마이그레이션 프로세스 중에 모든 게시된 API를 삭제해야 합니다.**
- **경고: 마이그레이션 프로세스에서 모든 봇의 100% 성공을 보장할 수 없습니다. 수동으로 다시 생성해야 할 경우를 대비해 중요한 봇 구성을 문서화하세요**

## 소개

### V3의 새로운 기능

V3는 Bedrock Chat에 다음과 같은 중요한 개선 사항을 도입했습니다:

1. **세분화된 권한 제어**: 사용자 그룹 기반 권한으로 봇에 대한 접근 제어
2. **봇 스토어**: 중앙화된 마켓플레이스를 통해 봇 공유 및 발견
3. **관리 기능**: API 관리, 봇을 필수로 표시, 봇 사용 분석

이러한 새로운 기능은 DynamoDB 스키마 변경을 필요로 하여, 기존 사용자를 위한 마이그레이션 프로세스가 필요합니다.

### 이 마이그레이션이 필요한 이유

새로운 권한 모델과 봇 스토어 기능을 위해 봇 데이터의 저장 및 접근 방식을 재구조화해야 했습니다. 마이그레이션 프로세스는 기존 봇과 대화를 새 스키마로 변환하면서 모든 데이터를 보존합니다.

> [!WARNING]
> 서비스 중단 안내: **마이그레이션 프로세스 중에는 모든 사용자에게 애플리케이션을 사용할 수 없습니다.** 사용자가 시스템에 접근할 필요가 없는 유지보수 시간에 이 마이그레이션을 수행하도록 계획하세요. 마이그레이션 스크립트가 성공적으로 완료되고 모든 데이터가 새 스키마로 적절히 변환된 후에만 애플리케이션을 다시 사용할 수 있습니다. 이 프로세스는 데이터 양과 개발 환경의 성능에 따라 일반적으로 약 60분이 소요됩니다.

> [!IMPORTANT]
> 마이그레이션 진행 전 주의사항: **마이그레이션 프로세스는 모든 봇에 대해 100% 성공을 보장할 수 없습니다**, 특히 이전 버전이나 맞춤 구성으로 생성된 봇의 경우 그렇습니다. 수동으로 재생성해야 할 경우에 대비해 중요한 봇 구성(지침, 지식 소스, 설정)을 마이그레이션 프로세스 시작 전에 문서화하세요.

## 마이그레이션 프로세스

### V3에서의 봇 가시성에 대한 중요 알림

V3에서는 **공개 공유가 활성화된 모든 v2 봇이 봇 스토어에서 검색 가능합니다.** 민감한 정보를 포함하는 봇을 발견되지 않게 하려면 V3로 마이그레이션하기 전에 비공개로 설정하는 것을 고려하세요.

### 1단계: 환경 이름 식별

이 절차에서 `{YOUR_ENV_PREFIX}`는 CloudFormation 스택의 이름을 식별하는 데 사용됩니다. [여러 환경 배포](../../README.md#deploying-multiple-environments) 기능을 사용하는 경우, 마이그레이션할 환경의 이름으로 대체하세요. 그렇지 않은 경우 빈 문자열로 대체하세요.

### 2단계: 저장소 URL 업데이트 (권장)

저장소 이름이 `bedrock-claude-chat`에서 `bedrock-chat`으로 변경되었습니다. 로컬 저장소를 업데이트하세요:

```bash
# 현재 원격 URL 확인
git remote -v

# 원격 URL 업데이트
git remote set-url origin https://github.com/aws-samples/bedrock-chat.git

# 변경 확인
git remote -v
```

### 3단계: 최신 V2 버전인지 확인

> [!WARNING]
> V3로 마이그레이션하기 전에 반드시 v2.10.0으로 업데이트해야 합니다. **이 단계를 건너뛰면 마이그레이션 중 데이터 손실이 발생할 수 있습니다.**

마이그레이션을 시작하기 전에 V2의 최신 버전(**v2.10.0**)을 실행 중인지 확인하세요:

```bash
# 최신 태그 가져오기
git fetch --tags

# 최신 V2 버전으로 체크아웃
git checkout v2.10.0

# 최신 V2 버전 배포
cd cdk
npm ci
npx cdk deploy --all
```

### 4단계: V2 DynamoDB 테이블 이름 기록

CloudFormation 출력에서 V2 ConversationTable 이름 가져오기:

```bash
# V2 ConversationTable 이름 가져오기
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableName'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

나중에 마이그레이션 스크립트에 필요하므로 이 테이블 이름을 안전한 곳에 저장해 두세요.

### 5단계: DynamoDB 테이블 백업

계속 진행하기 전에 방금 기록한 이름으로 DynamoDB ConversationTable의 백업을 생성하세요:

```bash
# V2 테이블 백업 생성
aws dynamodb create-backup \
  --no-cli-pager \
  --backup-name "BedrockChatV2Backup-$(date +%Y%m%d)" \
  --table-name YOUR_V2_CONVERSATION_TABLE_NAME

# 백업 상태가 사용 가능한지 확인
aws dynamodb describe-backup \
  --no-cli-pager \
  --query BackupDescription.BackupDetails \
  --backup-arn YOUR_BACKUP_ARN
```

### 6단계: 모든 게시된 API 삭제

> [!IMPORTANT]
> V3를 배포하기 전에 업그레이드 프로세스 중 Cloudformation 출력 값 충돌을 방지하기 위해 모든 게시된 API를 삭제해야 합니다.

1. 관리자로 애플리케이션에 로그인
2. 관리자 섹션으로 이동하여 "API 관리" 선택
3. 모든 게시된 API 목록 검토
4. 각 게시된 API 옆의 삭제 버튼을 클릭하여 삭제

API 게시 및 관리에 대한 자세한 정보는 [PUBLISH_API.md](../PUBLISH_API_ko-KR.md), [ADMINISTRATOR.md](../ADMINISTRATOR_ko-KR.md) 문서를 참조하세요.

### 7단계: V3 가져오기 및 배포

최신 V3 코드 가져오기 및 배포:

```bash
git fetch
git checkout v3
cd cdk
npm ci
npx cdk deploy --all
```

> [!IMPORTANT]
> V3를 배포하면 마이그레이션 프로세스가 완료될 때까지 모든 사용자가 애플리케이션을 사용할 수 없습니다. 새 스키마는 이전 데이터 형식과 호환되지 않으므로 다음 단계의 마이그레이션 스크립트를 완료할 때까지 사용자는 봇이나 대화에 액세스할 수 없습니다.

### 8단계: V3 DynamoDB 테이블 이름 기록

V3를 배포한 후 새로운 ConversationTable 및 BotTable 이름을 가져와야 합니다:

```bash
# V3 ConversationTable 이름 가져오기
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='ConversationTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack

# V3 BotTable 이름 가져오기
aws cloudformation describe-stacks \
  --output text \
  --query "Stacks[0].Outputs[?OutputKey=='BotTableNameV3'].OutputValue" \
  --stack-name {YOUR_ENV_PREFIX}BedrockChatStack
```

> [!Important]
> 마이그레이션 스크립트에 필요하므로 이전에 저장한 V2 테이블 이름과 함께 이 V3 테이블 이름을 반드시 저장해 두세요.

### 9단계: 마이그레이션 스크립트 실행

마이그레이션 스크립트는 V2 데이터를 V3 스키마로 변환합니다. 먼저 마이그레이션 스크립트 `docs/migration/migrate_v2_v3.py`를 편집하여 테이블 이름과 리전을 설정하세요:

```python
# DynamoDB가 위치한 리전
REGION = "ap-northeast-1" # 귀하의 리전으로 대체

V2_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableXXXX" # 4단계에서 기록한 값으로 대체
V3_CONVERSATION_TABLE = "BedrockChatStack-DatabaseConversationTableV3XXXX" # 8단계에서 기록한 값으로 대체
V3_BOT_TABLE = "BedrockChatStack-DatabaseBotTableV3XXXXX" # 8단계에서 기록한 값으로 대체
```

그런 다음 백엔드 디렉터리에서 Poetry를 사용하여 스크립트를 실행하세요:

> [!NOTE]
> Python 요구 사항 버전이 3.13.0 이상으로 변경되었습니다 (향후 개발에서 변경될 수 있음. pyproject.toml 참조). venv를 다른 Python 버전으로 설치한 경우 한 번 제거해야 할 수 있습니다.

```bash
# 백엔드 디렉터리로 이동
cd backend

# 아직 설치하지 않았다면 종속성 설치
poetry install

# 먼저 드라이 런을 실행하여 마이그레이션될 내용 확인
poetry run python ../docs/migration/migrate_v2_v3.py --dry-run

# 모든 것이 좋아 보이면 실제 마이그레이션 실행
poetry run python ../docs/migration/migrate_v2_v3.py

# 마이그레이션이 성공적으로 수행되었는지 확인
poetry run python ../docs/migration/migrate_v2_v3.py --verify-only
```

마이그레이션 스크립트는 현재 디렉터리에 마이그레이션 프로세스에 대한 세부 정보가 있는 보고서 파일을 생성합니다. 모든 데이터가 올바르게 마이그레이션되었는지 이 파일을 확인하세요.

#### 대용량 데이터 처리

많은 사용자 또는 대량의 데이터가 있는 환경의 경우 다음 접근 방식을 고려하세요:

1. **개별 사용자 마이그레이션**: 대용량 데이터를 가진 사용자의 경우 한 번에 한 명씩 마이그레이션:

   ```bash
   poetry run python ../docs/migration/migrate_v2_v3.py --users user-id-1 user-id-2
   ```

2. **메모리 고려 사항**: 마이그레이션 프로세스는 데이터를 메모리에 로드합니다. 메모리 부족(OOM) 오류가 발생하면 다음을 시도해 보세요:

   - 한 번에 한 명의 사용자 마이그레이션
   - 더 많은 메모리가 있는 머신에서 마이그레이션 실행
   - 사용자 배치를 나누어 마이그레이션

3. **마이그레이션 모니터링**: 대용량 데이터셋의 경우 생성된 보고서 파일을 확인하여 모든 데이터가 올바르게 마이그레이션되었는지 확인하세요.

### 10단계: 애플리케이션 확인

마이그레이션 후 애플리케이션을 열고 다음 사항을 확인하세요:

- 모든 봇을 사용할 수 있는지
- 대화가 보존되었는지
- 새로운 권한 제어가 작동하는지

### 정리 (선택 사항)

마이그레이션이 성공적이었고 모든 데이터가 V3에서 제대로 접근 가능한지 확인한 후, 선택적으로 V2 대화 테이블을 삭제하여 비용을 절감할 수 있습니다:

```bash
# V2 대화 테이블 삭제 (마이그레이션 성공 확인 후에만)
aws dynamodb delete-table --table-name YOUR_V2_CONVERSATION_TABLE_NAME
```

> [!IMPORTANT]
> 모든 중요한 데이터가 V3로 성공적으로 마이그레이션되었음을 철저히 확인한 후에만 V2 테이블을 삭제하세요. 원본 테이블을 삭제하더라도 마이그레이션 후 몇 주 동안은 2단계에서 생성한 백업을 보관하는 것이 좋습니다.

## V3 자주 묻는 질문

### 봇 접근 및 권한

**Q: 내가 사용 중인 봇이 삭제되거나 접근 권한이 제거되면 어떻게 되나요?**
A: 인증은 채팅 시점에 확인되므로, 즉시 접근이 차단됩니다.

**Q: 사용자가 삭제되면(예: 직원 퇴사) 어떻게 되나요?**
A: 해당 사용자의 ID를 파티션 키(PK)로 사용하여 DynamoDB의 모든 항목을 삭제함으로써 데이터를 완전히 제거할 수 있습니다.

**Q: 필수 공개 봇의 공유를 해제할 수 있나요?**
A: 아니요, 관리자가 먼저 해당 봇을 필수가 아닌 것으로 표시해야 공유를 해제할 수 있습니다.

**Q: 필수 공개 봇을 삭제할 수 있나요?**
A: 아니요, 관리자가 먼저 해당 봇을 필수가 아닌 것으로 표시해야 삭제할 수 있습니다.

### 보안 및 구현

**Q: 봇 테이블에 행 수준 보안(RLS)이 구현되어 있나요?**
A: 아니요, 다양한 접근 패턴을 고려하여 구현하지 않았습니다. 봇에 접근할 때 권한 부여를 수행하며, 메타데이터 유출 위험은 대화 기록에 비해 최소한입니다.

**Q: API를 게시하기 위한 요구 사항은 무엇인가요?**
A: 봇이 공개되어 있어야 합니다.

**Q: 모든 개인 봇을 관리할 수 있는 화면이 있을 예정인가요?**
A: 초기 V3 릴리스에는 없습니다. 그러나 필요에 따라 사용자 ID로 쿼리하여 항목을 삭제할 수 있습니다.

**Q: 더 나은 검색 경험을 위한 봇 태깅 기능이 있을 예정인가요?**
A: 초기 V3 릴리스에는 없지만, 향후 업데이트에서 LLM 기반 자동 태깅이 추가될 수 있습니다.

### 관리

**Q: 관리자는 무엇을 할 수 있나요?**
A: 관리자는 다음을 수행할 수 있습니다:

- 공개 봇 관리 (고비용 봇 확인 포함)
- API 관리
- 공개 봇을 필수로 표시

**Q: 부분 공유 봇을 필수로 만들 수 있나요?**
A: 아니요, 공개 봇만 지원합니다.

**Q: 고정된 봇의 우선순위를 설정할 수 있나요?**
A: 초기 릴리스에서는 불가능합니다.

### 인증 구성

**Q: 인증은 어떻게 설정하나요?**
A:

1. Amazon Cognito 콘솔에서 BrChat 사용자 풀에 사용자 그룹 생성
2. 필요에 따라 사용자를 그룹에 추가
3. BrChat에서 봇 공유 설정을 구성할 때 접근을 허용할 사용자 그룹 선택

참고: 그룹 멤버십 변경 시 다시 로그인해야 합니다. 변경 사항은 토큰 새로 고침 시 반영되지만, ID 토큰 유효 기간(V3에서 기본 30분, `cdk.json` 또는 `parameter.ts`의 `tokenValidMinutes`로 구성 가능) 동안에는 반영되지 않습니다.

**Q: 시스템이 봇에 접근할 때마다 Cognito에 확인하나요?**
A: 아니요, 불필요한 I/O 작업을 피하기 위해 JWT 토큰을 사용하여 권한을 확인합니다.

### 검색 기능

**Q: 봇 검색에서 의미론적 검색을 지원하나요?**
A: 아니요, 부분 텍스트 일치만 지원합니다. 의미론적 검색(예: "automobile" → "car", "EV", "vehicle")은 현재 OpenSearch Serverless의 제약으로 인해 사용할 수 없습니다(2025년 3월 기준).