import time
import threading
import requests
from storage import network_storage

global time_to_sync
time_to_sync = 5 # tempo entre as sincronizações

clock_lock = threading.Lock()
clock = {
  "time": 0, # tempo do relógio
  "drift": 1, # drift do relógio
  "update_time": time.time() # tempo da última atualização
}

def get_time_sync():
  return time_to_sync

def set_time_sync(new_time):
  global time_to_sync
  time_to_sync = new_time

def get_max_time_since_last_update():
  return get_time_sync()*2 + get_time_sync() + (network_storage.get_self_id()*2) # tempo máximo desde a última atualização do relógio

def set_update_time():
  clock_lock.acquire()
  clock["update_time"] = time.time()
  clock_lock.release()

def get_time() -> int:
  clock_lock.acquire()
  time = clock["time"]
  clock_lock.release()
  return time

def set_time(new_time: int):
  clock_lock.acquire()
  clock["time"] = new_time
  clock_lock.release()
  
def increment_time():
  clock_lock.acquire()
  clock["time"] += 1
  clock_lock.release()
  
def get_drift() -> int:
  clock_lock.acquire()
  drift = clock["drift"]
  clock_lock.release()
  return drift

def set_drift(new_drift: int):
  clock_lock.acquire()
  clock["drift"] = new_drift
  clock_lock.release()

def increment_time_background():
  while True:
    increment_time()
    time.sleep(get_drift())

def send_time():
  while True:
    # verifica se o tempo máximo de sincronização foi atingido
    time_since_last_update = time.time() - clock["update_time"]
    if (time_since_last_update > get_max_time_since_last_update()):
      # o relógio atual é o líder
      network_storage.set_leader(network_storage.get_self_id())
      print(f"ID clock que realizou a detecção: {network_storage.get_self_id()}.\n Tempo máximo de sincronização atingido. Já se passaram {time_since_last_update} segundos desde a última atualização do relógio.\nTempo máximo de espera: {get_max_time_since_last_update()}")
      
    if network_storage.is_self_leader():
      print('Enviando os tempos')
      #enviar uma requisição de sincronização para todos a cada 5 segundos  
      for addr in network_storage.clocks["addrs"]:
        # se o endereço for o próprio host, pula
        if addr == network_storage.find_addr_by_id(network_storage.get_self_id()):
          continue
        
        url = f"{addr}/time/{get_time()}/{network_storage.get_self_id()}/{get_time_sync()}"
        print(f"Enviando tempo para {url}")
        try:
          info_returned = requests.post(url=url)
          # se o relógio do host for maior que o relógio atual, ele se torna o novo líder
          if(info_returned.status_code == 403):
            print(f"O relógio do host {addr} é maior que o relógio atual. Ele se tornará o novo líder.")
            network_storage.set_leader(network_storage.get_id_from_addr(addr))
            break
          
          # se deu tudo certo, atualiza o tempo do relógio
          set_update_time()
        except Exception as e:
          print(e)
          pass
      time.sleep(get_time_sync())