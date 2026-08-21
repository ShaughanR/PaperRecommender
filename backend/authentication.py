from datetime import datetime, timedelta, timezone
from backend.sensitive_info import secret_key, algorithm, access_token_expire_minutes
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials



def create_access_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=access_token_expire_minutes
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(
        payload,
        secret_key,
        algorithm=algorithm
    )


def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=[algorithm]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication token"
            )

        return int(user_id)

    except (JWTError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token"
        )


security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    return verify_token(token)


