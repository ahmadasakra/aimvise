from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_dashboard():
    """Get dashboard data"""
    return {"stats": {"total_analyses": 0, "active_analyses": 0}} 