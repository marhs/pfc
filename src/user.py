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
        self.mAuth = []

        # Valores del sistema
        self.publicUsers = []
        self.publicRandoms = dict()
        self.publicValues = []

        # Estado del usuario. 
        self.state = 0
    
    def register(self,subkey):
        # La implementacion del registro se deja abierta
        self.subkey = subkey 

    def isLeader(self):
        return self.leader == 1

    def compruebaDatosDeUser(self,numEstado):
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
            msgdata = self.generateRandom()
            self.recibeRandom(self.name,msgdata)
            data = [2,self.name,'broadcast',msgdata]
        if s == 3:
            self.recoverKey()
            msgdata = self.computeHi()
        
            if not self.compruebaAuth(self.mAuth):
                self.error(1)
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
            if not self.compruebaH(msgData):
                self.error(0)
            self.recoverMsg(msgData)

    def recibeRandom(self, user, random):
        self.publicRandoms[user] = random
        return self.state
    
    def compruebaH(self, mensaje):
        men = []
        # mensaje = [m1,m2,...,mn,Auth]
        for n in mensaje:
            if n[1] == self.name:
                men = n    

        ui = self.name
        ri = self.random
        si = self.subkey

        g = men[0]
        sol = hs([ui, g, si, ri])

        return men[2] == sol

    def generateRandom(self):
        self.random = getrandbits(512)
        return self.random
    
    # Coge el mensaje M y devuelve el g si+r correspondiente al usuario. 
    def recoverMsg(self, m): 
        self.mAuth = m
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

    def clear(self):
        self.state = 0

    def compruebaAuth(self, mensajes):
        gs = []
        for mensaje in mensajes[:-1]:
            gs.append(mensaje[0])
        b = self.publicUsers
        a = []
        c = []
        for user in b:
            c.append(self.publicRandoms[user])

        sol1 = hs([self.key]+gs+b+c) 
        sol2 = mensajes[len(mensajes)-1]
        return sol1 == sol2

    def error(self, estado):
        errorList = { 0 : 'No se puede verificar el mensaje de confirmacion',
                      1 : 'No se puede verificar el mensaje de autenticacion',
                      2 : 'Se ha recibido un mensaje que no correspondia'} 

        return estado in errorList
