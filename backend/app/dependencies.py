import json
import logging
import os
from functools import wraps
from typing import Optional

import boto3
from app.auth import verify_token
from app.user import User, UserMembership
from fastapi import Depends, HTTPException, status, Header, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
import requests

from app.usecases.group import (
    is_user_authorized,
    fetch_all_groups_by_user_id
)

# Import ACTION_CONFIG_MAP and ROLE_HIERARCHY
from app.routes.schemas.group import ACTION_CONFIG_MAP, ROLE_HIERARCHY

security = HTTPBearer()

logger = logging.getLogger(__name__)

cognito_client = boto3.client("cognito-idp")

# Cache for JWK
JWK = None
CLIENT_ID = os.environ.get("CLIENT_ID", "")

def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    # Initialize variables
    token_audience = None
    expected_audience = None
    decoded = None # Initialize decoded as well

    try:
        # 1. Initial Unverified Decode & Logging
        try:
            # Tell the initial decode to ignore audience AND signature for inspection purposes
            token_contents = jwt.decode(token.credentials, key="", options={"verify_signature": False, "verify_aud": False})
            token_audience = token_contents.get("aud", "Not found in token")
            expected_audience = CLIENT_ID or "Not Set from Env"

            # Log types and representations before verification attempt
            logger.debug(f"Pre-verification - Token 'aud' type: {type(token_audience)}, repr: {repr(token_audience)}")
            logger.debug(f"Pre-verification - Expected 'aud' type: {type(expected_audience)}, repr: {repr(expected_audience)}")
            if token_audience != expected_audience:
                 logger.warning(f"Pre-verification - AUDIENCE MISMATCH DETECTED. Token 'aud': {repr(token_audience)}, Expected: {repr(expected_audience)}")
            else:
                 logger.debug(f"Pre-verification - Audiences appear to match: {repr(token_audience)}")

        except JWTError as initial_decode_err:
             logger.error(f"Error during *initial unverified* decode: {initial_decode_err}", exc_info=True)
             # Re-raise to be caught by the outer handler, but log specifics here
             raise initial_decode_err
        except Exception as initial_err:
             logger.error(f"Unexpected error during initial decode/setup: {initial_err}", exc_info=True)
             raise # Let outer handler deal with it

        # 2. Attempt Verified Decode (where the error seems to happen)
        try:
            logger.debug("Attempting verified token decoding with verify_token...")
            decoded = verify_token(token.credentials) # This is the call raising "Invalid audience"
            logger.debug("Verified token decoding successful.")
        except JWTError as verification_err:
            # Log specifically when verify_token fails
            logger.error(f"Error *during* verify_token call: {verification_err}", exc_info=True)
            # Log the state again, *immediately* after verify_token failed
            logger.error(f"State at verify_token failure - Token 'aud': {repr(token_audience)}, Expected: {repr(expected_audience)}")
            # Re-raise the error to be handled by the outer JWTError handler
            raise verification_err
        except Exception as verify_e:
             logger.error(f"Unexpected error during verify_token call: {verify_e}", exc_info=True)
             raise # Let outer handler deal with it

        # --- If verification succeeds ---
        user_id = decoded["sub"]
        user_name = decoded["cognito:username"]
        cognito_group_names = decoded.get("cognito:groups", [])

        logger.debug(f"User {user_id} ({user_name}) authenticated. Cognito Groups: {cognito_group_names}")

        # Fetch internal groups/roles from database
        memberships_list = []
        try:
            internal_groups_data = fetch_all_groups_by_user_id(user_id)
            logger.debug(f"Fetched {len(internal_groups_data)} internal group memberships for user {user_id}")
            # Add internal groups/roles (with group_id)
            for group in internal_groups_data:
                 if hasattr(group, 'group_id') and hasattr(group, 'role'):
                     memberships_list.append(UserMembership(group_id=group.group_id, role=group.role))
                 else:
                     logger.warning(f"Internal group data for user {user_id} missing group_id or role: {group}")
        except Exception as e:
            logger.error(f"Failed to fetch internal groups for user {user_id}: {e}", exc_info=True)
            # Proceed without internal groups if fetch fails, but log error

        # Add Cognito groups/roles (without group_id)
        for group_name in cognito_group_names:
             memberships_list.append(UserMembership(role=group_name, group_id=None))

        logger.info(f"Final memberships for user {user_id}: {memberships_list}")

        # Return user information including merged memberships
        return User(
            id=user_id,
            name=user_name,
            memberships=memberships_list
        )
    # --- Outer Exception Handlers ---
    except JWTError as e:
        # This catches errors from initial decode OR re-raised from verify_token failure
        logger.warning(f"JWT Verification Error Handler reached: {str(e)}")
        error_detail = str(e)

        # Log audience info (might be None if initial decode failed)
        final_token_aud_repr = repr(token_audience) if token_audience is not None else "Unavailable (Initial decode failed?)"
        final_expected_aud_repr = repr(expected_audience) if expected_audience is not None else "Unavailable (Initial setup failed?)"

        if "audience" in error_detail.lower():
             logger.error(f"Final Handler - JWT Audience verification failed. Token 'aud': {final_token_aud_repr}, Expected: {final_expected_aud_repr}")
             # Update error detail based on potentially more accurate info from the handler decode - simplified now
             error_detail = f"Invalid token audience. Expected {final_expected_aud_repr} but got {final_token_aud_repr}."
        elif "expired" in error_detail.lower():
             logger.error("Final Handler - JWT Token has expired.")
             error_detail = "Token has expired."
        # Remove the previous re-decode logic here as it's less useful now with the nested try/except

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Could not validate credentials: {error_detail}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Catch any other unexpected errors during the process
    except Exception as e:
        logger.error(f"Outer Unexpected Error Handler reached: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred during authentication.",
            headers={"WWW-Authenticate": "Bearer"},
        )


def _check_permissions_core(user: User, action: str) -> bool:
    """Core logic to check if any user membership grants permission for the action."""
    action_permissions = ACTION_CONFIG_MAP.get(action)
    if not action_permissions:
        logger.error(f"Permission action '{action}' is not configured in ACTION_CONFIG_MAP. Denying access for user {user.id}.")
        return False

    if not hasattr(user, 'memberships') or not user.memberships:
        logger.warning(f"User {user.id} has no memberships for action '{action}'. Denying access.")
        return False

    # Iterate through all memberships (internal roles and Cognito groups)
    for membership in user.memberships:
        role_name = membership.role # Could be internal role or Cognito group name
        # Check if this role/group grants permission for the action
        if action_permissions.get(role_name, False):
            logger.info(f"User {user.id} granted action '{action}' via membership '{role_name}'.")
            return True # Permission granted by at least one membership

    # If loop completes without returning True, permission is denied
    logger.warning(f"User {user.id} denied action '{action}'. Memberships: {[m.role for m in user.memberships]}. Required: {action_permissions}")
    return False

def check_permission(action: str):
    """
    Dependency factory to check if the current user (from request state)
    has permission for a specific action based on ALL their memberships
    (internal roles + Cognito groups) and the ACTION_CONFIG_MAP.
    Raises HTTPException 403 if not authorized.
    """
    def dependency(request: Request) -> User:
        if not hasattr(request.state, 'current_user') or not request.state.current_user:
            logger.error("User not found in request state for permission check.")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not authenticated for permission check."
            )

        current_user: User = request.state.current_user

        # Use the new core checking logic
        if not _check_permissions_core(current_user, action):
            # Raise 403 if core logic returned False
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User not authorized for action '{action}'.")

        # If check passes, return the user object
        return current_user

    return dependency

def user_has_permission(user: User, action: str) -> bool:
    """Checks if a user object has permission for an action based on ACTION_CONFIG_MAP."""
    # Use the new core checking logic directly
    return _check_permissions_core(user, action)

def check_is_user_authorized(action: str, user: User = Depends(get_current_user)):
    # This function should likely be deprecated and replaced by check_permission dependency
    logger.warning("Deprecated function 'check_is_user_authorized' called. Use 'check_permission' dependency.")
    
    # Use the common helper function first
    if not user_has_permission(user, action): # user_has_permission now uses the new core logic
        logger.warning(f"User {user.id} denied action '{action}' via deprecated check.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User not authorized for action '{action}'.",
        )
    
    logger.info(f"User {user.id} authorized for '{action}' via deprecated check.")
    # Return user for compatibility if previous implementation did
    return user

def check_auth_secret(x_auth_secret: str = Header(...)):
    # ... existing implementation ...
    pass