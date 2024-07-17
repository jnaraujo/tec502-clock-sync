from fastapi import APIRouter
from utils import *
router = APIRouter()

@router.get("/", status_code=200)
def get_root_route():
    return {"message": "Welcome to the API!"}

#function to set new drift to this time counter
@router.patch('/drift-set/{drift}')
def set_drift_clock(drift: float):
    set_drift(drift)

#function to set new time
@router.patch('/time-set/{time}')
def set_time_clock(time: float):
    set_time(time)

#rota para apresentação na interface os dados do relogio
@router.get('/infos-clock')
def get_time_host():
    return {'time': get_time(),
            'is_leader':  get_is_leader(),
            'id_clock': get_id(),
            'drif': get_drift()
            }

