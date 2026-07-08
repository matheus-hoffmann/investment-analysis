from fastapi import APIRouter


router = APIRouter()


@router.get("/check")
def verify_api_stability():
    return "API is working"