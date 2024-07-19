from fastapi import APIRouter, HTTPException
router = APIRouter()

@router.get("/", status_code=200)
def get_root_route():
    return {"message": "Welcome to the API!"}
