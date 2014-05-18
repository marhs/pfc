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
        self.k = calculaClave(self.key,GENERATOR,MODULUS)
        self.subk  = dict()
        self.active = 0

        self.objUsuarios = []
        self.state = 0
        self.numUsers = users

    def getData(self):
        s = self.state
        if s == 0:
            return False
        elif s == 1:
            return self.users
        elif s == 2:
            return self.randoms
        elif s == 3:
            return self.sendMessage()


    def addUser(self,user):
    # Inicio de protocolo, limpia los parametros activos

        self.users.append(user)
        self.subkeys[user] = self.generateSubKey()
        #if len(self.users) == self.numUsers:
        #    self.state += 1
            # TODO Enviar users()
        return self.state

    # Empieza en S1 y al acabar pasa a S2.
    def recibeRandom(self, user, random):
        self.randoms[user] = random
        if len(self.randoms) == self.numUsers:
            self.state += 1
            # TODO Enviar randoms()
        return self.state
            

    def resetUserRdy(self):
        self.active = 0
        return self.active

    def userRdy(self):
        self.active += 1
        if self.active == self.numUsers:
            self.state += 1
            self.resetUserRdy()
        print ' [Active]', self.active ,'/',self.numUsers
        return self.state
    # Genera S
    def generateKey(self, keySize):
        s = getrandbits(self.keySize)
        self.k = calculaClave(s,GENERATOR,MODULUS)
        print '    CLAVE:',self.k
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

        for user in range(self.numUsers):
            self.message.append(self.generarMensajeUsuario(user))
        self.message.append(self.generateAuth())
        return self.message

    # Genera Mi, para cada uno de los usuarios, dado su indice. 
    def generarMensajeUsuario(self,indice):
        ui = self.users[indice]
        ri = self.randoms[ui]
        si = self.subkeys[ui]
        si1 = self.key - si

        g = calculaClave(si1+ri,GENERATOR,MODULUS)
        self.subk[ui] = g
        h = [ui,g,si,ri]
        print '    GenH:',h
        hashMsg = hs(h)
        message = [g,ui,hashMsg]
        return message

    # Genera el mensaje final Auth
    def generateAuth(self):
        b = self.users
        a = []
        c = []
        for user in b:
            c.append(self.randoms[user])
            a.append(self.subk[user])

        return hs([self.k]+a+b+c)

    # Devuelve si' (la que se envia, creo)
    def getSubKey(self, user):
        return self.key - self.subkeys[user] 


    def generateHi(self,user):
        res = [self.subkeys[user],self.k]
        res = res + self.users
        for n in self.users:
            res.append(self.randoms[n])
        return hs(res)

    # Comprueba si el hi recibido desde user es correcto y el que deberia ser
    # en caso de que todos los users pasen esto, finaliza el protocolo
    def checkHi(self, msg, user):
        if self.generateHi(user) == msg:
            self.active += 1
            if self.active == len(self.users):
                self.finish(1)
            return 4
        else:
            self.finish(0)
            return 0


    # Operaciones de finalizacion del intercambio
    def finish(self, st):
        # TODO Cerrar todos los sockets de comunicacion. 
        if st != 1:
            return False
        # TODO Devolver por pantalla la clave. 
        print '[FIN] Acuerdo de clave completo. '
        print '      Clave:',self.k
        self.state = 5

        return True
