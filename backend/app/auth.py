import os
import dotenv
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

dotenv.load_dotenv()

CLERK_JWKS_URL = os.getenv("CLERK_JWKS_URL")

if not CLERK_JWKS_URL:
    raise RuntimeError("CLERK_JWKS_URL environment variable is not set.")

AUTHORIZED_PARTIES = {"http://localhost:3000"}

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
        claims = jwt.decode(token, signing_key.key, algorithms=["RS256"])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    azp = claims.get("azp")
    if azp is not None and azp not in AUTHORIZED_PARTIES:
        raise HTTPException(status_code=401, detail="Invalid token origin")

    return claims["sub"]
