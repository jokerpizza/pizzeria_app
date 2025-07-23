from fastapi import APIRouter

router = APIRouter()

@router.get("/balance")
def balance():
    return {"card": 0.0, "cash": 0.0}
