from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.jwt_handler import verify_access_token
from app.database.dependencies import get_db
from app.models.user import User


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or Expired Token"
        )

    user_identifier = payload.get("sub")

    if not user_identifier:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token Payload"
        )

    user = db.query(User).filter(
        User.email == user_identifier
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user