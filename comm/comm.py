# Objeto communication
# Es el encargado de gestionar la comunicacion entre participantes y kgc
from user import User 
from kgc import KeyGenerationCenter

class Comm():

    def __init__(self, kgc, participantes):

        self.kgc = kgc
        self.participants = self.generateParticipants(participantes)
        self.messages = []
    
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
        for n in range(states):
            # Empiezan los participantes
            for participant in self.participants:
                #print 'Bucle',n, 'user', participant.name
                self.routeMsg(participant.send_message())
            # Turno del KGC
            self.routeMsg(self.kgc.send_message())

        return self.kgc.secret


## TEST ZONE ##
"""
kgc = KeyGenerationCenter(1024,4) 
comm = Comm(kgc,4)
comm.bucle()

print comm.participants[0].key
print comm.kgc.k
for m in comm.messages:
    print m
"""
