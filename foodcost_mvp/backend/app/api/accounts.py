from fastapi import APIRouter

router = APIRouter()

@router.get("/open")
def open_accounts():
    return []
