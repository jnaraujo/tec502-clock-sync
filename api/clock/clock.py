import time

clock = {
  "time": 0,
  "shift": 1
}

def get_time() -> int:
  return clock["time"]

def set_time(new_time: int):
  clock["time"] = new_time
  
def increment_time():
  clock["time"] += 1
  
def get_shift() -> int:
  return clock["shift"]

def set_shift(new_shift: int):
  clock["shift"] = new_shift
    
def increment_time_background():
  while True:
    increment_time()
    time.sleep(get_shift())