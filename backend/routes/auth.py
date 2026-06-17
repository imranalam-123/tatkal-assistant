from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Header
)

from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from backend.schemas.user import UserCreate
from backend.database import get_db

from backend.services.auth_service import (
    create_user,
    authenticate_user
)

from backend.auth import (
    create_access_token,
    verify_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.get("")
def test_auth():
    return {
        "message": "Auth route working"
    }


@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        new_user = create_user(db, user)

        return {
            "message": "User registered successfully",
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = authenticate_user(
        db,
        form_data.username,   # email entered in Swagger
        form_data.password
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {
            "sub": db_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email
        }
    }


@router.get("/me")
def get_current_user(
    authorization: str = Header(
        default=None,
        alias="Authorization"
    )
):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )

    token = authorization.replace(
        "Bearer ",
        ""
    )

    payload = verify_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return {
        "message": "Protected route accessed",
        "user_email": payload.get("sub")
    }


# DEBUG ROUTE
@router.get("/users")
def get_users(
    db: Session = Depends(get_db)
):
    from backend.models.user import User

    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "password": user.password
        }
        for user in users
    ]