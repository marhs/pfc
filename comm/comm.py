# Objeto communication
# Es el encargado de gestionar la comunicacion entre participantes y kgc
from user import User 
from kgc import KeyGenerationCenter
from time import time

class Comm():

    def __init__(self, kgc, participantes):

        self.kgc = kgc
        self.participants = self.generateParticipants(participantes)
        self.messages = []
        self.time = 0
        
        return None

    def clear(self):

        self.messages = []
        self.registerMessages = []
        
        return True

    def generateParticipants(self,numParticipantes):
        
        res = []
        res.append(User('Usuario 0',leader=1))
        self.userRegister(res[0])
        res[0].publicUsers = []
        for n in range(numParticipantes):
            res[0].publicUsers.append('Usuario '+str(n))

        for n in range(1,numParticipantes):
            u = User('Usuario '+str(n))
            res.append(u)
            self.userRegister(u)
        return res
    
    def userRegister(self,user):
        
        #msg = [10,'kgc',user.name,rsaData]
        
        
        subkey = self.kgc.register(user.name)
        user.register(subkey)
        
        return user
    

    def routeMsg(self,mensaje):
        if mensaje == []:
            return False
        self.messages.append(mensaje)
        #print '[Mensaje]', mensaje
        msgId = mensaje[0]
        msgSrc = mensaje[1]
        msgDst = mensaje[2]
        msgData = mensaje[3]
        
        receivers = [self.kgc]
        receivers.extend(self.participants)
        
        for rec in receivers:
            if msgSrc != rec.name and (msgDst == 'broadcast' or msgDst == rec.name):
                rec.receive_message(mensaje)


    def bucle(self):
        states = 3
        start_time = time()
        for n in range(states):
            if n == 0:
                self.kgc.clear()
            # Empiezan los participantes
            for participant in self.participants:
                if n == 0:
                    participant.clear()
                #print 'Bucle',n, 'user', participant.name
                self.routeMsg(participant.send_message())
            # Turno del KGC
            self.routeMsg(self.kgc.send_message())
        self.time = time() - start_time
        
        return self.kgc.secret

# Testea que se produzca el intercambio de clave correctamente entre todos
def test(numUsers):
    kgc = KeyGenerationCenter() 
    comm = Comm(kgc,numUsers)
    # Efectua el intercambio de clave
    for n in range(2):
        comm.bucle()
        print '[kgc]',comm.kgc.k
        print '[usrk]',comm.participants[0].key
        print '[usrs]',comm.participants[0].subkey
    # Comprueba que se haya efectuado convenientemente. 
    key = comm.kgc.k
    for n in comm.participants:
        assert n.key == key
    return comm.time
    return True

import matplotlib.pyplot as plt
def testTime(a,b, mean=1, step=1):
    times = []
    for n in range(a,b):
        if n%step != 0:
            continue
        print 'Test', n
        if mean == 1:
            times.append(test(n))
        else:
            time_aux = []
            for m in range(mean):
                time_aux.append(test(n))
            times.append(sum(time_aux)/len(time_aux))
    plt.plot(times)
    plt.ylabel('Tiempo (s)')
    plt.xlabel('Numero de participantes')
    plt.show()
    return times
