import logging
import os
import boto3
from jose import jwt, jwk
import httpx
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Request, HTTPException
from fastapi import Form
from app.repositories.lti_data import get_lti_data
router = APIRouter(tags=["lti"])

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# TODO - Hard code values for now. Will move to configuration later. 
CANVAS_ISSUER = 'https://canvas.instructure.com'  # Canvas base URL
CANVAS_JWK_URL = 'https://sso.canvaslms.com/api/lti/security/jwks'
CANVAS_OIDC_AUTH_URL = 'https://sso.canvaslms.com/api/lti/authorize_redirect'

REGION = os.environ.get("REGION", "us-east-1")
USER_POOL_ID = os.environ.get("USER_POOL_ID")
FRONTEND_URL = os.environ.get("FRONTEND_URL")


@router.post("/lti/connect")
async def lti_connect(
    request: Request,
    iss: str = Form(),
    login_hint: str = Form(),
    client_id: str = Form(),
    lti_deployment_id: str = Form(),
    lti_message_hint: str = Form(),
):
    """Handle connect request sent to OIDC Initiation Endpoint used by LTI protocol."""

    # Lookup lti_deployment_id in database
    rsp = get_lti_data(lti_deployment_id)
    if rsp is None or 'client_id' not in rsp:
        logger.error(f'Error: LTI table lookup with {lti_deployment_id} got response {rsp}')
        raise HTTPException(status_code=400, detail="Invalid LTI deployment ID or client ID not found")

    expected_client_id = rsp['client_id']

    if iss != CANVAS_ISSUER or client_id != expected_client_id:
        logger.error(f'Error: iss = {iss}, expected {CANVAS_ISSUER}, client_id = {client_id}, expected {expected_client_id}')
        raise HTTPException(status_code=400, detail="Invalid issuer or client ID")
    
    TOOL_REDIRECT_URI = str(request.base_url)[:-1] + '/lti/redirect'

    # TODO generate a random nonce and store with TTL
    nonce = 'CHANGETHISVALUE'
    redirect_url = f"{CANVAS_OIDC_AUTH_URL}?client_id={client_id}&login_hint={login_hint}&scope=openid&response_type=code&redirect_uri={TOOL_REDIRECT_URI}&response_mode=form_post&nonce={nonce}&prompt=none&lti_message_hint={lti_message_hint}"

    logger.info(f'Redirecting to: {redirect_url}')
    return RedirectResponse(url=redirect_url, status_code=302)

def lookup_user(cognito, user_pool_id, email):
    response = cognito.list_users(
        UserPoolId=user_pool_id,
        Filter=f'email = "{email}"'
    )
    return response['Users'][0] if response['Users'] else None

def create_user(cognito, user_pool_id, email, password):
    response = cognito.admin_create_user(
        UserPoolId=user_pool_id,
        Username=email,
        UserAttributes=[
            { 'Name': 'email', 'Value': email },
            { 'Name': 'email_verified', 'Value': 'true' }
        ],
        TemporaryPassword=password, 
        MessageAction='SUPPRESS'
    )

    # Set the permanent password
    cognito.admin_set_user_password(
        UserPoolId=user_pool_id,
        Username=email,
        Password=password,
        Permanent=True
    )
    return response['User']

def lookup_or_create_user(email):
    # TODO - use a random password
    PASSWORD = '1@Random'

    cognito_client = boto3.client('cognito-idp', region_name=REGION) 
    user = lookup_user(cognito_client, USER_POOL_ID, email)
    if user:
        logger.info(f'Existing user {user}')
    else:
        logger.info(f'Creating new user with email {email}')
        user = create_user(cognito_client, USER_POOL_ID, email, PASSWORD)
    return user


@router.post("/lti/redirect")
async def lti_redirect(
    request: Request,
    id_token: str = Form(),
):
    """Handle redirect request from OIDC Authorization Endpoint as part of LTI protocol."""
    try:
        # Get key id from token header
        kid = jwt.get_unverified_header(id_token)['kid']
        
        # Fetch JWK from Canvas
        canvas_jwt_response = httpx.get(CANVAS_JWK_URL).json()
        public_key = next((key for key in canvas_jwt_response['keys'] if key['kid'] == kid), None)
        
        if not public_key:
            raise HTTPException(status_code=400, detail="No matching key found")

        # Convert JWK to PEM and verify token
        pem = jwk.construct(public_key).to_pem()
        options = {'verify_aud': False}
        decoded_token = jwt.decode(id_token, pem, options=options, issuer=CANVAS_ISSUER)
        logger.info(f'Decoded token: {decoded_token}')
        
        # Extract claims
        course_name = decoded_token.get('https://purl.imsglobal.org/spec/lti/claim/context', {}).get('label', None)
        roles = decoded_token.get('https://purl.imsglobal.org/spec/lti/claim/roles', [])
        # remove prefix http://purl.imsglobal.org/vocab/lis/v2 from roles
        roles = [r.replace('http://purl.imsglobal.org/vocab/lis/v2/', '') for r in roles]
        email = decoded_token.get('email', None)
        name = decoded_token.get('name', None)
        platform = decoded_token.get('https://purl.imsglobal.org/spec/lti/claim/tool_platform', {})
        course_id = decoded_token.get('https://purl.imsglobal.org/spec/lti/claim/custom', {}).get('canvas_course_id', None)
        deployment_id = decoded_token.get('https://purl.imsglobal.org/spec/lti/claim/deployment_id', None)
        group_id = f'{deployment_id}-{course_id}'

        # Find the Cognito user corresponding to the email address. Create a new user if user doesn't exist
        user = lookup_or_create_user(email)

        payload = {
            "sub": user['Username'],
            "email": email,
            "name": name,
            "roles": roles,
            "platform": platform,
            "deploymentId": deployment_id,
            "courseName": course_name,
            "courseId": course_id,
            "groupId": group_id,
        }

        import urllib.parse
        query_params = urllib.parse.urlencode(payload)
        redirect_url = f"{FRONTEND_URL}/lti?{query_params}"

        return RedirectResponse(url=redirect_url, status_code=302)

    except jwt.JWTError as e:
        raise HTTPException(status_code=400, detail=f"Invalid LTI launch request: {str(e)}")

