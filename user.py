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
            return self.generateRandom()
        if s == 2:
            return 'OK'
    def generateRandom(self):
        self.random = getrandbits(KEYSIZE)
        self.state += 1
        return self.random
    
    def recoverKey(self, kgc):
        
        self.subkey = kgc.sendSubKey(self.name)
        return self.subkey
    
    def recoverMsg(self, m): 
         
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


