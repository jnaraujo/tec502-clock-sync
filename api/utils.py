import threading
from time import sleep
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
id_clock = 1


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



def start_threads():
    timer_update = threading.Thread(target=update_time, daemon=True)
    timer_update.start()
    leader_send = threading.Thread(target=update_time, daemon=True)
    leader_send.start()


start_threads()