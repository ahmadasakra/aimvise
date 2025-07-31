from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_reports():
    """List analysis reports"""
    return {"reports": []} 