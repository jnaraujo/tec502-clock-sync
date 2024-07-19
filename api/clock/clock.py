import time
import threading
import requests
from storage import network_storage

#lock para impedir que o valor seja alterado em 2 threads diferentes ao mesmo tempo
time_lock = threading.Lock()
is_sync = False

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

def set_is_sync(ocurring_status):
  global is_sync
  is_sync = ocurring_status


def increment_time_background():
  while True:
    if(not is_sync):
      increment_time()
      time.sleep(get_drift())


def prepare_to_send_time():
      print('Enviando os tempos')
      #enviar uma requisição de sincronização para todos a cada 5 segundos  
      for addr in network_storage.clocks["addrs"]:
        print(f"Addr: {addr} - {network_storage.find_addr_by_id(network_storage.get_self_id())}")
        if addr == network_storage.find_addr_by_id(network_storage.get_self_id()):
          print("Pulando o próprio host")
          continue
        
        url = f"{addr}/leader-sync-make"
        print(f"Enviando para {url}")
        try:
          info_returned = requests.post(url=url)
          if(info_returned.status_code == 403):
            print(f"O tempo do id {network_storage.get_id_from_addr(addr)} é menor que o tempo atual")
            network_storage.set_leader(network_storage.get_id_from_addr(addr))
            break
        except Exception as e:
          print(e)
          print(f"host: {addr} saiu da rede")
          pass


def send_time_complete():
      #enviar uma requisição de sincronização para todos a cada 5 segundos  
      for addr in network_storage.clocks["addrs"]:
        print(f"Addr: {addr} - {network_storage.find_addr_by_id(network_storage.get_self_id())}")
        if addr == network_storage.find_addr_by_id(network_storage.get_self_id()):
          print("Pulando o próprio host")
          continue
        
        url = f"{addr}/leader-sync-complete"
        print(f"Enviando para {url}")
        try:
          info_returned = requests.post(url=url)
          if(info_returned.status_code == 403):
            print(f"O tempo do id {network_storage.get_id_from_addr(addr)} é menor que o tempo atual")
            network_storage.set_leader(network_storage.get_id_from_addr(addr))
            break
        except Exception as e:
          print(e)
          print(f"host: {addr} saiu da rede")
          pass


def send_time():
  while True:
    if network_storage.is_self_leader():
      prepare_to_send_time()
      print('Enviando os tempos')
      #enviar uma requisição de sincronização para todos a cada 5 segundos  
      for addr in network_storage.clocks["addrs"]:
        print(f"Addr: {addr} - {network_storage.find_addr_by_id(network_storage.get_self_id())}")
        if addr == network_storage.find_addr_by_id(network_storage.get_self_id()):
          print("Pulando o próprio host")
          continue
        
        url = f"{addr}/time/{get_time()}/{network_storage.get_self_id()}"
        print(f"Enviando para {url}")
        try:
          info_returned = requests.post(url=url)
          if(info_returned.status_code == 403):
            print(f"O tempo do id {network_storage.get_id_from_addr(addr)} é menor que o tempo atual")
            network_storage.set_leader(network_storage.get_id_from_addr(addr))
            break
        except Exception as e:
          print(e)
          print(f"host: {addr} saiu da rede")
          pass
      send_time_complete()
      time.sleep(5)

