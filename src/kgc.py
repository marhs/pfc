from random import SystemRandom
from random import getrandbits
from utils import *

class KeyGenerationCenter:
    """
        Nota: El control de errores de este modulo, asi como el de los
              usuarios, no esta terminado.
    """

    def __init__(self):

        self.name = 'kgc'
        self.keySize = 1536
        self.secret = 0 

        self.state = 0

        self.users = []
        self.randoms = dict()
        self.subkeys = dict()

        # Parametros del intercambio
        self.message = []
        self.auth = []
        self.k = 0 
        self.subk  = dict() 

        self.iniciaClave()
    
        # Cuando hay que esperar varios mensajes. 
        self.active = 0
    
    def register(self,user):
        return self.addUser(user)

    def compruebaDatosDeEstado(self, numEstado):
        # TODO El control de errores de este protocolo no esta terminado
        self.state += 1
        return self.state 

    def iniciaClave(self):
        
        self.secret = self.generateKey(self.keySize) 
        for n in self.subkeys:
            if self.subkeys[n] > self.secret:
                self.iniciaClave()


        self.k = calculaClave(self.secret,GENERATOR,MODULUS) 

    # Cambia al estado siguiente y envia el mensaje. \
    def send_message(self):
        # Comprueba si tiene todo lo necesario para el estado actual
        # If todo correcto, s++
        if self.compruebaDatosDeEstado(self.state) == -1 :
            return False
        # Ejecuta las acciones y devuelve los datos. 
        
        s = self.state

        # Hay que tener en cuenta que estoy trabajando con el estado de abajo
        if s == 1:
            # Envia el mensaje 1, BROADCAST
            msgdata = self.users
            data = [1,'kgc','broadcast',msgdata]
        elif s == 2:
            # Envia M,Auth - BROADCAST
            msgdata = self.generaMensaje()
            data = [3,'kgc','broadcast',msgdata]
        elif s == 3:
            data = []
        return data

    def descomponeCabeceras(self, message):
        msgId = message[0]
        msgSrc = message[1]
        msgDst = message[2]
        msgData = message[3]

        return (msgId, msgSrc, msgDst, msgData)

    def receive_message(self, message):

        msgId, msgSrc, msgDst, msgData = self.descomponeCabeceras(message)
        if msgId == 0:
            self.numUsers = len(msgData)
            for n in msgData:
                self.addUser(n)
        elif msgId == 2:
            # Recibe los randoms ri
            self.randoms[msgSrc] = msgData
        elif msgId == 4:
            # Recibe el h'i
            self.checkHi(msgData,msgSrc)
    
    # Empieza en S1 y al acabar pasa a S2.
    def recibeRandom(self, user, random):
        self.randoms[user] = random

        return self.state

    def addUser(self,user):
        #print 'Adding user', user
    # Inicio de protocolo, limpia los parametros activos
        if user in self.users:
            return True
        self.users.append(user)
        self.subkeys[user] = self.generateSubKey()
        
        return self.subkeys[user]

    def resetUserRdy(self):
        self.active = 0
        return self.active

    def userRdy(self):
        self.active += 1
        if self.active == self.numUsers:
            self.state += 1
            self.resetUserRdy()
        return self.state
    # Genera S
    def generateKey(self, keySize):
        s = getrandbits(self.keySize)
        self.k = calculaClave(s,GENERATOR,MODULUS)
        return s


    # Divide S en 2 partes y lo devuelve (usado en la anterior)
    def generateSubKey(self):

        subkey = getrandbits(self.keySize)
        while subkey > self.secret:
            subkey = getrandbits(self.keySize-100)

        return subkey

    # Genera M = [M1,M2,M3...]
    def generaMensaje(self):

        for user in range(self.numUsers):
            self.message.append(self.generarMensajeUsuario(user))
        self.message.append(self.generateAuth())
        return self.message

    # Genera Mi, para cada uno de los usuarios, dado su indice. 
    def generarMensajeUsuario(self,indice):
        ui = self.users[indice]
        ri = self.randoms[ui]
        si = self.subkeys[ui]
        si1 = self.secret - si

        g = calculaClave(si1+ri,GENERATOR,MODULUS)
        self.subk[ui] = g
        h = [ui,g,si,ri]
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
        return self.secret - self.subkeys[user] 


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
            return True
        else:
            self.finish(0)
            return 0

    def clear(self):
        self.state = 0
        self.iniciaClave()

