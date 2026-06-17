from fastapi import APIRouter, Depends

from backend.dependencies.auth_dependency import (
    get_current_user
)

router = APIRouter(
    prefix="/train",
    tags=["Train"]
)


@router.post("/search")
def search_train(
    source: str,
    destination: str,
    journey_date: str,
    current_user=Depends(get_current_user)
):
    return {
        "message": "Train search successful",
        "searched_by": current_user.email,
        "source": source,
        "destination": destination,
        "journey_date": journey_date,
        "trains": [
            {
                "train_no": "12301",
                "train_name": "Rajdhani Express",
                "available": True
            },
            {
                "train_no": "12260",
                "train_name": "Duronto Express",
                "available": False
            }
        ]
    }