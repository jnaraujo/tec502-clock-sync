import time
import threading
import requests
from storage import network_storage

#lock para impedir que o valor seja alterado em 2 threads diferentes ao mesmo tempo
time_lock = threading.Lock()
counter_lock = threading.Lock()
is_sync = False
global received_time_by_leader
global time_to_sync
global counter_timeout
counter_timeout = 0
time_to_sync = 5
received_time_by_leader = False

clock = {
  "time": 0,
  "drift": 1
}

def get_counter_timeout():
  global counter_timeout
  counter_lock.acquire()
  counter = counter_timeout
  counter_lock.release()
  return counter

def set_counter_timeout(counter):
  global counter_timeout
  counter_lock.acquire()
  counter_timeout = counter
  counter_lock.release()

def increment_counter():
  global counter_timeout
  counter_lock.acquire()
  counter_timeout += 1
  counter_lock.release()

def get_received_time_by_leader():
  return received_time_by_leader

def set_received_time_by_leader(received):
  global received_time_by_leader
  received_time_by_leader = received

def get_time_to_sync():
  global time_to_sync
  return time_to_sync

def set_time_to_sync(new_time:int) -> int:
  global time_to_sync
  time_to_sync = new_time

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
      time.sleep(get_time_to_sync())

#bug aq, ele parece q n zera, na verdade ele 0, conta dnv

def time_out_leader_msg():
  time_to_counter = 7 + (network_storage.get_self_id()*2)
  global counter
  while True:
    if (get_received_time_by_leader()):
      time.sleep(1)
      increment_counter()
      print("CONTADOR DO TIMEOUT: ", get_counter_timeout())
      #se ele receber uma nova atualização do lider durante a execução do for
      if(get_counter_timeout() >= time_to_counter):
        if(not verify_my_conection()):
          set_counter_timeout(0) 
          network_storage.set_leader(network_storage.get_self_id())
        else:
          set_counter_timeout(0) 
          set_received_time_by_leader(False)


#verificar se o host em questão encontra-se conectado
def verify_my_conection():
  for addr in network_storage.clocks["addrs"]:
    print(f"Addr: {addr} - {network_storage.find_addr_by_id(network_storage.get_self_id())}")
    if addr == network_storage.find_addr_by_id(network_storage.get_self_id()):
      print("Pulando o próprio host")
      continue
    
    url = f"{addr}/clock"
    print(f"Enviando para {url}")
    try:
      info_returned = requests.get(url=url)
      if(info_returned.status_code == 200):
        return 1
    except Exception as e:
      print(e)
      print(f"host: {addr} saiu da rede")
      pass
    finally:
      return 0