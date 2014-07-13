from random import SystemRandom
from random import getrandbits
from utils import *

# Parametros en comun, grupo generador, etc
GENERATOR = 17
#MODULUS   = getrandbits(1024)
MODULUS   = 156431412343


KEYSIZE = 128

class User:

    def __init__(self, name):
        self.name = name
        self.random = -1 
        self.key = -1
        self.subkey = -1

        # Msg = M,Auth
        self.msg = []

        # Valores del sistema
        self.publicUsers = []
        self.publicRandoms = []
        self.publicValues = []

        # Estado del usuario. 
        self.state = 0

    def compruebaDatosDeUser(numEstado):
        self.state += 1
        return self.state 
    
    def send_message(self):

        # Comprueba que los datos para dicho estado esten correctamente. 
        if compruebaDatosDeUser(self.state) == -1:
            return False

        s = self.state
        data = []
        if s == 1:
            # Envia la lista de participantes si es el lider
            # if isLeader()...
            data = []
        if s == 2:
            # self.checklistParticipants() TODO Add condicion de parada
            data = self.generateRandom()
        if s == 3:
            data = self.computeHi()
        
        return data

## A partir de aqui todo es jauja
    
    def generateRandom(self):
        self.random = getrandbits(KEYSIZE)
        return self.random
    
    # Coge el mensaje M y devuelve el g si+r correspondiente al usuario. 
    # Ahora toca JSON JSON JSON 
    def recoverMsg(self, m): 
        # Recorremos los M sin el Auth. 
        for n in m[:-1]: 
            self.publicValues.append(n[0])
            self.publicUsers.append(n[1])
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

