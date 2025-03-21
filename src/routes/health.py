from fastapi.routing import APIRouter
from starlette import status


router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint with system status"""
    return {"status": "OK"}
