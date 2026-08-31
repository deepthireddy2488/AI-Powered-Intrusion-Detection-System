from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from datetime import timedelta
from app.schemas.user_schema import UserLogin
from app.core.security import verify_password
from app.core.jwt_handler import create_access_token
from app.core.dependencies import get_current_user

from app.schemas.user_schema import UserRegister
from app.database.dependencies import get_db
from app.repositories.user_repository import (
    create_user,
    get_user_by_email,
)
from app.core.security import hash_password

router = APIRouter()




@router.post("/register")
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    existing_user = get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)

    create_user(
        db=db,
        full_name=user.full_name,
        email=user.email,
        password=hashed_password
    )

    return {
        "message": "User registered successfully"
    }





@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    existing_user = get_user_by_email(db, user.email)

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )

    if not verify_password(
        user.password,
        existing_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )

    token = create_access_token(
        {
            "sub": existing_user.email
        },
        expires_delta=timedelta(hours=1)
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }








@router.get("/me")
def get_profile(
    current_user=Depends(get_current_user)
):

    return {
        "message": "Access Granted",
        "user": current_user
    }




#  venv\Scripts\activate
#  uvicorn app.main:app --reload
#  python -m uvicorn app.main:app --reload
# deepthireddy4690@gmail.com 24d24d24d