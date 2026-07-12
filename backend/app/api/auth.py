from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session
from app.core.dependencies import get_current_user

from app.db.database import get_db
from app.models.user import User
from app.schemas.auth import RegisterSchema
from app.core.security import hash_password
from app.schemas.auth import LoginSchema
from app.core.security import (
    verify_password,
    create_access_token
)

router = APIRouter()


@router.post("/register")
def register(user: RegisterSchema, db: Session = Depends(get_db)):
    try:
        existing = db.query(User).filter(
            User.email == user.email
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        new_user = User(
            username=user.username,
            email=user.email,
            password=hash_password(user.password)
        )

        db.add(new_user)
        db.commit()

        return {"message": "User created"}

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
        
        
@router.post("/login")
def login(
    credentials: LoginSchema,
    db: Session = Depends(get_db)
):
    try:
        user = db.query(User).filter(
            User.email == credentials.email
        ).first()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        if not verify_password(
            credentials.password,
            user.password
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        access_token = create_access_token(
            data={"sub": str(user.id)}
        )

        return {"access_token": access_token}

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
    
from app.core.dependencies import get_current_user

@router.get("/me")
def me(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role
    }
    