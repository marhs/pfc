from random import SystemRandom
from random import getrandbits
from utils import *

class User:

    def __init__(self, name, leader=0):
        self.name = name
        self.random = -1 
        self.key = -1
        self.subkey = -1
        self.leader = leader
        # Msg = M,Auth
        self.msg = []

        # Valores del sistema
        self.publicUsers = []
        self.publicRandoms = dict()
        self.publicValues = []

        # Estado del usuario. 
        self.state = 0
    
    # TODO Se supone que esto es seguro
    def register(self,subkey):
        self.subkey = subkey 

    def isLeader(self):
        return self.leader == 1

    def compruebaDatosDeUser(self,numEstado):
        # TODO Comprobar que para estado se cumplen las condiciones antes de
        #      pasar al siguiente
        self.state += 1
        return self.state 
    
    def send_message(self):

        # Comprueba que los datos para dicho estado esten correctamente. 
        if self.compruebaDatosDeUser(self.state) == -1:
            return False

        s = self.state
        data = []
        if s == 1:
            # Envia la lista de participantes si es el lider
            if self.isLeader():
                data = [0,self.name,'kgc',self.publicUsers]
            else:
                data = []
        if s == 2:
            # self.checklistParticipants() TODO Add condicion de parada
            msgdata = self.generateRandom()
            self.recibeRandom(self.name,msgdata)
            data = [2,self.name,'broadcast',msgdata]
        if s == 3:
            self.recoverKey()
            msgdata = self.computeHi()
        
            data = [4,self.name,'kgc',msgdata]
        return data

    def descomponeCabeceras(self, message):
        msgId = message[0]
        msgSrc = message[1]
        msgDst = message[2]
        msgData = message[3]

        return (msgId, msgSrc, msgDst, msgData)

    def receive_message(self, message):

        msgId, msgSrc, msgDst, msgData = self.descomponeCabeceras(message)
        
        if msgId == 1:
            # Mensaje inicial
            # init(msgData) o algo asi
            if self.publicUsers == []:
                self.publicUsers = msgData
        elif msgId == 2:
            # Recibe los randoms ri de los otros.
            self.recibeRandom(msgSrc,msgData)
        elif msgId == 3:
            # Recibe el MAuth
            self.recoverMsg(msgData)

    def recibeRandom(self, user, random):
        self.publicRandoms[user] = random
        return self.state
            
## A partir de aqui todo es jauja
    
    def generateRandom(self):
        self.random = getrandbits(512)
        return self.random
    
    # Coge el mensaje M y devuelve el g si+r correspondiente al usuario. 
    def recoverMsg(self, m): 
        # Recorremos los M sin el Auth. 
        for n in m[:-1]: 
            self.publicValues.append(n[0])
            if n[1] == self.name:
                self.msg = n
        if self.msg:
            return self.msg
        else:
            return False

    def genH(self):
        r = [self.name, self.msg[0], self.subkey, self.random]
        return hs(r)

    def recoverKey(self):

        sr1 = calculaClave(self.subkey,GENERATOR,MODULUS)
        r1 = calculaClave(self.random,GENERATOR,MODULUS)
        self.key = keyRecover(sr1,self.msg[0],r1,MODULUS)
        return self.key

    def generateAuth(self):
        
        auth = [self.key]
        auth = auth + self.publicValues
        auth = auth + self.publicUsers

        for key in self.publicUsers:
            auth.append(self.publicRandoms[key])
                
        return hs(auth)

    def computeHi(self):

        res = [self.subkey,self.key]
        res = res + self.publicUsers
        for n in self.publicUsers:
            res.append(self.publicRandoms[n])

        return hs(res)
    # TODO
    def compruebaH(self):

        return False

    # TODO
    def compruebaAuth(self):

        return False

    # Finaliza acuerdo de clave
    def finish(self):

        print '[FIN] Acuerdo de clave completo. '
        print '      Clave:',self.key

        return True

