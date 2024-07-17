from fastapi import APIRouter
from utils import set_drift, set_time
router = APIRouter()

@router.get("/", status_code=200)
def get_root_route():
    return {"message": "Welcome to the API!"}

#function to set new drift to this time counter
@router.patch('/drift-set/{drift}')
def set_drift_clock(drift: float):
    set_drift(drift)

@router.patch('/time-set/{time}')
def set_time_clock(time: float):
    set_time(time)