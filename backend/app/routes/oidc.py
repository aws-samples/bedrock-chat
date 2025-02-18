from fastapi import APIRouter, Request, HTTPException
from fastapi import Form
router = APIRouter(tags=["oidc"])


@router.post("/oidc/connect")
async def oidc_connect(
    request: Request,
    iss: str = Form(),
    login_hint: str = Form(),
    client_id: str = Form(),
    lti_deployment_id: str = Form(),
    lti_message_hint: str = Form(),
):
    """Handle connect request sent to OIDC Initiation Endpoint."""
    # return a page that contains all the parameters passed in 
    return { "iss": iss, "login_hint": login_hint, "client_id": client_id, "lti_deployment_id": lti_deployment_id, "lti_message_hint": lti_message_hint }



@router.post("/oidc/redirect")
async def oidc_redirect(
    request: Request,
    id_token: str = Form(),
):

    # return a page that contains all the parameters passed in 
    return { "id_token": id_token }


