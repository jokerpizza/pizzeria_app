from fastapi import APIRouter

router = APIRouter()

@router.get("/recent")
def recent_documents():
    return []
