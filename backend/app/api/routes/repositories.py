from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_repositories():
    """List analyzed repositories"""
    return {"repositories": []} 