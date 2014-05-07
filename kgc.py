from random import SystemRandom
from random import getrandbits
from utils import *

# Parametros en comun, grupo generador, etc
GENERATOR = 17
#MODULUS   = getrandbits(1024)
MODULUS   = 15643

KEYSIZE = 128

class KeyGenerationCenter:

    def __init__(self, keySize, users):
        self.keySize = keySize
        self.key = self.generateKey(keySize)
        self.users = []
        self.randoms = dict()
        self.subkeys = dict()
        self.message = []
        self.auth = []
        self.k = 0
        self.active = 0

        self.objUsuarios = []
        self.state = 0
        self.numUsers = users

    def getData(self):
        s = self.state
        if s == -1:
            return self.users
        elif s == 0:
            return self.randoms
        elif s == 1:
            return message

    def addUser(self,user):
    # Inicio de protocolo, limpia los parametros activos

        self.users.append(user)
        if len(self.users) == self.numUsers:
            self.state += 1
            # TODO Enviar users()
        return self.state

    # Empieza en S1 y al acabar pasa a S2.
    def recibeRandom(self, user, random):
        self.randoms[user] = random
        if len(self.randoms) == self.numUsers:
            self.state += 1
            # TODO Enviar randoms()
        return self.randoms
            
    # Genera S
    def generateKey(self, keySize):
        s = getrandbits(self.keySize)
        self.k = calculaClave(s,GENERATOR,MODULUS)
        return s

    # Divide S en 2 partes por cada usuario. 
    def generateSubKeys(self):
        # Primero limpia las subclaves que pudiesen existir
        self.subkeys = dict()
        for client in self.users:
            key = self.generateSubKey()
            self.subkeys[client] = key

        return self.users

    # Divide S en 2 partes y lo devuelve (usado en la anterior)
    def generateSubKey(self):

        subkey = getrandbits(self.keySize)
        while subkey > self.key:
            subkey = getrandbits(self.keySize)

        return subkey

    def sendMessage(self):

        for user in range(len(self.users)):
            self.message.append(self.generarMensajeUsuario(user))
        self.message.append(self.generateAuth())
        return self.message

    # Genera Mi, para cada uno de los usuarios, dado su indice. 
    def generarMensajeUsuario(self,indice):
        ri = self.randoms[indice]
        ui = self.users[indice]
        si = self.subkeys[ui]
        si1 = self.key - si

        g = calculaClave(si+ri,GENERATOR,MODULUS)
        h = [ui,g,si1,ri]
        hashMsg = hs(h)
        message = [g,ui,hashMsg]
        return message

    # Genera el mensaje final Auth
    def generateAuth(self):
        a = self.message
        b = self.users
        c = self.randoms
        return hs([self.k,a,b,c])

    # Devuelve si' (la que se envia, creo)
    def getSubKey(self, user):
        return self.key - self.subkeys[user] 
