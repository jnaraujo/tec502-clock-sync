'''
    def global variates
'''

#indica se o host em questão é o lider
global is_leader

#indica o drift para aquele relogio
global drift

global time

def set_drift(new_drift):
    global drift
    drift = new_drift


def set_time(new_time):
    global time
    time = new_time
    
    