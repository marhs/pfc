from random import SystemRandom
from random import getrandbits
from utils import *

# Parametros en comun, grupo generador, etc
GENERATOR = 17
#MODULUS   = getrandbits(1024)
MODULUS   = 15643

KEYSIZE = 128

class User:

    def __init__(self, name):
        self.name = name
        self.random = -1 
        self.subkey = -1
        self.key = -1
        self.msg = []

        self.publicUsers = []
        self.publicRandoms = []
        self.publicValues = []

        self.state = 0
    # Una vez se tiene el mensaje que envia el KGC, se recupera la clave.

    def getData(self):
        s = self.state
        if s == 0:
            self.state += 1
            return self.name
        if s == 1:
            self.state +=1
            return 'ACK'
        if s == 2:
            self.state += 1
            return self.generateRandom()
        if s == 3:
            self.state += 1
            return 'ACK'
        if s == 4:
            # TODO Add conditionals to pass
            return self.computeHi()
        
        ## Espero que se haya hecho el recover msg


    
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
            print self.msg
            return self.msg
        else:
            return False

    def genH(self):
        r = [self.name, self.msg[0], self.subkey, self.random]
        return hs(r)

    def recoverKey(self):

        print self.msg
        print type(self.msg)
        sr1 = calculaClave(self.subkey,GENERATOR,MODULUS)
        r1 = calculaClave(self.random,GENERATOR,MODULUS)
        self.key = keyRecover(sr1,self.msg[0],r1,MODULUS)
        print self.key
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

        print res
        return hs(res)
    # TODO
    def compruebaH(self):

        return False

    # TODO
    def compruebaAuth(self):

        return False

