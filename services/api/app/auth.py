import secrets
from urllib.parse import urlencode

from fastapi import APIRouter, HTTPException, Query, Response

from app.config import settings
from app.security import OAuthState

router = APIRouter(prefix="/auth", tags=["auth"])
oauth_state = OAuthState(settings.oauth_state_secret)


@router.get("/google/start")
def google_start(response: Response) -> dict[str, str]:
    nonce = secrets.token_urlsafe(24)
    state = oauth_state.issue(nonce)
    response.set_cookie("oauth_state", state, httponly=True, secure=settings.app_env != "development", samesite="lax", max_age=600)
    query = urlencode({"client_id": "configured-at-runtime", "redirect_uri": "/auth/google/callback", "response_type": "code", "scope": "openid email profile", "state": state})
    return {"authorization_url": f"https://accounts.google.com/o/oauth2/v2/auth?{query}"}


@router.get("/google/callback")
def google_callback(state: str = Query(min_length=1), code: str = Query(min_length=1)) -> dict[str, str]:
    try:
        oauth_state.verify(state)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="invalid oauth state") from exc
    return {"status": "code_received", "code_length": str(len(code))}
