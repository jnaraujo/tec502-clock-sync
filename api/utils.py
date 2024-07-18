import os
import threading
from time import sleep
import requests


'''
    def global variates
'''

#indica se o host em questão é o lider
global is_leader

#indica o drift para aquele relogio
global drift

#é o tempo daquele relogio
global time


'''
    inicialização das variaveis
'''
is_leader = False
drift = 0.1
time = 0
id_clock = 0


'''
    lista dos hosts com seus IDs
        dicionario no formato: 
            {id: endereço:porta}
'''

dict_hosts = {
    1: "http://localhost:8080",
    2: "http://localhost:8081",
    3: "http://localhost:8082",
    4: "http://localhost:8083"
}

dict_hosts[1] = os.getenv('clock_1')
dict_hosts[2] = os.getenv('clock_2')
dict_hosts[3] = os.getenv('clock_3')
dict_hosts[4] = os.getenv('clock_4')
id_clock = int(os.getenv('id_clock'))
print(dict_hosts)
#lock para impedir que o valor seja alterado em 2 threads diferentes ao mesmo tempo
time_lock = threading.Lock()

def set_drift(new_drift):
    global drift
    drift = new_drift


def set_time(new_time):
    global time
    if(new_time >= time):
        time_lock.acquire()
        time = new_time
        time_lock.release()
        #indica que o novo horario recebido foi maior ou igual e ele atualiza o dele
        return 1 
    else:
        #indica que o tempo esta inferior ao dele, ele tem que verificar o novo lider
        return 0
    

def set_leader(leader):
    global is_leader
    is_leader = leader
    

def get_time():
    global time
    return time

def get_is_leader():
    global is_leader
    return is_leader

def get_id():
    return id_clock

def get_drift():
    global drift
    
    return drift


def leader_send_time():
    global is_leader
    while True:
        if(is_leader):
            #enviar uma requisição de sincronização para todos a cada 5 segundos
            sleep(5)
            for host in dict_hosts:
                url = f"{dict_hosts[host]}/time-set/{get_time()}"
                try:
                    info_returned = requests.patch(url=url)
                    if(info_returned.status_code == 200):
                        #se entrou aqui é o outro host aceitou isso e isso confirma que ele ainda é o leader
                        is_leader = True
                        pass
                    else:
                        is_leader = False
                        break
                except:
                    print(f"host: {host} saiu da rede")
                    pass




def update_time():
    global time
    global drift
    while True:
        sleep(drift)
        time_lock.acquire()
        time += 1
        time_lock.release()
        print(f"Meu drift é: {drift}, e o meu tempo é: {time}")



def start_system():
    global is_leader
    timer_update = threading.Thread(target=update_time, daemon=True)
    timer_update.start()
    leader_send = threading.Thread(target=update_time, daemon=True)
    leader_send.start()
    if(id_clock == 1):
        sleep(2)
        is_leader = True


start_system()