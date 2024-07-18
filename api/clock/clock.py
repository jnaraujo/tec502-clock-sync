import time

clock = {
  "time": 0,
  "drift": 1
}

def get_time() -> int:
  return clock["time"]

def set_time(new_time: int):
  clock["time"] = new_time
  
def increment_time():
  clock["time"] += 1
  
def get_drift() -> int:
  return clock["drift"]

def set_drift(new_drift: int):
  clock["drift"] = new_drift
    
def increment_time_background():
  while True:
    increment_time()
    time.sleep(get_drift())