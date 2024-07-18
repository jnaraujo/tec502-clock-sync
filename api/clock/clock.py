import time
import threading
import requests
from storage import network_storage

#lock para impedir que o valor seja alterado em 2 threads diferentes ao mesmo tempo
time_lock = threading.Lock()


clock = {
  "time": 0,
  "drift": 1
}

def get_time() -> int:
  return clock["time"]

def set_time(new_time: int):
  time_lock.acquire()
  clock["time"] = new_time
  time_lock.release()
  
def increment_time():
  time_lock.acquire()
  clock["time"] += 1
  time_lock.release()
  
def get_drift() -> int:
  return clock["drift"]

def set_drift(new_drift: int):
  clock["drift"] = new_drift
    
def increment_time_background():
  while True:
    increment_time()
    time.sleep(get_drift())


def send_time():
    while True:
        if network_storage.is_self_leader():
            print('BBBBBB')
            #enviar uma requisição de sincronização para todos a cada 5 segundos
            
            for addr in network_storage.clocks["addrs"]:
                if addr == network_storage.get_addrs()[network_storage.get_self_id()]:
                   continue
                
                print('CCCC')
                url = f"{addr}/time/{get_time()}/{network_storage.get_self_id()}"
                print(f'TO MANDANDO VIU: {url}')
                try:
                    info_returned = requests.post(url=url)
                    if(info_returned.status_code == 403):
                        network_storage.set_leader(network_storage.get_id_from_addr(addr))
                except Exception as e:
                    print(e)
                    print(f"host: {addr} saiu da rede")
                    pass
            time.sleep(5)