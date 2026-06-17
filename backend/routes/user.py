from fastapi import APIRouter, Depends
from backend.dependencies.auth_dependency import get_current_user

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.get("/profile")
def get_profile(
    current_user=Depends(get_current_user)
):
    return {
        "message": "User profile fetched successfully",
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email
        }
    }


@router.get("/dashboard")
def dashboard(
    current_user=Depends(get_current_user)
):
    return {
        "message": f"Welcome {current_user.username}",
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email
        }
    }