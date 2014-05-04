# Protocolo de comparticion de claves

# SystemRandom usa el generador de numeros aleatorios del sistema
# /dev/urandom
# es una clase envoltura de os.urandom
from random import SystemRandom
from random import getrandbits
from utils import *

# Parametros en comun, grupo generador, etc
GENERATOR = 17
#MODULUS   = getrandbits(1024)
MODULUS   = 15643

KEYSIZE = 128


class KeyGenerationCenter:

    def __init__(self, keySize):
        self.keySize = keySize
        self.key = self.generateKey(keySize)
        self.users = []
        self.randoms = []
        self.subkeys = dict()
        self.message = []
        self.auth = []
        self.k = 0
        self.active = 0

        self.objUsuarios = []

    def recibeUsuarios(self, listaUsuarios):
    # Inicio de protocolo, limpia los parametros activos
    # TODO Implementar la autenticacion aqui
        self.users, self.randoms, self.objUsuarios = [],[],[]

        self.objUsuarios = listaUsuarios
        for usuario in listaUsuarios:
            self.users.append(usuario.name)
        return self.users

    def recibeRandoms(self):
        self.randoms = []
        for user in self.objUsuarios:
            self.randoms.append(user.generateRandom())
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

    def generateAuth(self):
        a = self.message
        b = self.users
        c = self.randoms
        return hs([self.k,a,b,c])

    def sendSubKey(self, user):
        return self.key - self.subkeys[user] 

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

    # Una vez se tiene el mensaje que envia el KGC, se recupera la clave.
    def generateRandom(self):
        self.random = getrandbits(KEYSIZE)
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

## Test zone


# Inicia un generador de claves
kgc = KeyGenerationCenter(KEYSIZE)

# Genera 8 usuarios ficticios
users = []
for n in range(8):
    users.append(User("Name"+str(n)))

# Computa las comunicaciones entre el KGC y los usuarios
kgc.recibeUsuarios(users) # Recibe la informacion de los usuarios
kgc.recibeRandoms()       # Recibe los parametros aleatorios de cada uno
kgc.generateSubKeys()     # Genera las subclaves si' + si

print("Secreto:   ", kgc.key)
print("Usuarios:  ", kgc.users)
print("Randoms:")
for n in range(len(kgc.randoms)):
    print('     ',kgc.users[n],kgc.randoms[n])

print("Subclaves:")
for n in range(len(kgc.randoms)):
    print('     ',kgc.users[n],kgc.subkeys[kgc.users[n]])
    
print("Mensaje:   ")
msg = kgc.sendMessage()
mostrarMensaje(msg)

auth = msg[len(msg)-1]
print('Auth: ',auth)


for user in users:
    user.recoverKey(kgc)
    user.recoverMsg(msg)
    print('Hash user',user.genH())

    






