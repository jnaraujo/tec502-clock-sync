clocks = {
  "addrs": [],
  "leader": -1,
}

def get_addrs() -> list:
  return clocks["addrs"]

def set_addrs(new_addrs: list):
  clocks["addrs"] = new_addrs
  
def get_leader() -> int:
  return clocks["leader"]

def get_leader_addr() -> str:
  return clocks["addrs"][get_leader()]

def set_leader(new_leader: int):
  clocks["leader"] = new_leader
  
def add_addr(addr: str):
  clocks["addrs"].append(addr)
  
def remove_addr(addr: str):
  clocks["addrs"].remove(addr)