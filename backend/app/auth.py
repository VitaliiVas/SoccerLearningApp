import os
import dotenv
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

dotenv.load_dotenv()

CLERK_JWKS_URL = os.getenv("CLERK_JWKS_URL")

if not CLERK_JWKS_URL:
    raise RuntimeError("CLERK_JWKS_URL environment variable is not set.")

AUTHORIZED_PARTIES = {
    origin.strip()
    for origin in os.getenv("AUTHORIZED_PARTIES", "http://localhost:3000").split(",")
    if origin.strip()
}

# Clerk user IDs allowed to create, edit and delete lessons.
ADMIN_CLERK_IDS = {
    clerk_id.strip()
    for clerk_id in os.getenv("ADMIN_CLERK_IDS", "").split(",")
    if clerk_id.strip()
}

jwks_client = jwt.PyJWKClient(CLERK_JWKS_URL)
security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> str:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Missing bearer token")

    token = credentials.credentials

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        # Clerk session tokens live ~60s, so a few seconds of clock skew
        # between Clerk and this server would otherwise cause random 401s.
        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            leeway=5,
        )
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    azp = claims.get("azp")
    if azp is not None and azp not in AUTHORIZED_PARTIES:
        raise HTTPException(status_code=401, detail="Invalid token origin")

    sub = claims.get("sub")
    if not sub:
        raise HTTPException(status_code=401, detail="Invalid token")

    return sub


def require_admin(clerk_id: str = Depends(get_current_user)) -> str:
    if clerk_id not in ADMIN_CLERK_IDS:
        raise HTTPException(status_code=403, detail="Admin access required")

    return clerk_id
