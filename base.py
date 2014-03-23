# Protocolo de comparticion de claves

# SystemRandom usa el generador de numeros aleatorios del sistema
# /dev/urandom
# es una clase envoltura de os.urandom
from random import SystemRandom
from random import getrandbits

# Parametros en comun, grupo generador, etc
GENERATOR = 3
MODULUS   = 15

def calculaClave(secret):
    return pow(GENERATOR, secret, MODULUS)



class KeyGenerationCenter:

    def __init__(self, keySize):
        self.keySize = keySize
        self.key = self.generateKey(keySize)
        self.users = []
        self.randoms = []
        self.subkeys = []
        self.messages = []
        self.auth = []
        self.k = 0
        self.active = 0

        self.objUsuarios = []

    def recibeUsuarios(self, listaUsuarios):
        # Inicio de protocolo, limpia los parametros activos
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

        return getrandbits(self.keySize)

    # Divide S en 2 partes por cada usuario. 
    def generateSubKeys(self):
        # Primero limpia las subclaves que pudiesen existir
        self.subkeys = []
        for client in self.users:
            key = self.generateSubKey()
            self.subkeys.append(key)

        return self.users

    # Divide S en 2 partes y lo devuelve (usado en la anterior)
    def generateSubKey(self):

        subkey = getrandbits(self.keySize)
        while subkey > self.key:
            subkey = getrandbits(self.keySize)

        return subkey

    def sendMessage(self):
        '''
        for user in range(len(self.users)):
            g = 13^(self.subkeys[user]+self.random[user]) # TODO Averiguar como se hace la operacion g^x
            # Hash
            hs = [self.users[user],0,0,0]
            self.message.append([g,self.users[user],hs])
        '''
        return self.message

    def generateAuth(self):
        '''
        a = self.generateSubKs()
        b = self.users
        c = self.randoms
        return [self.k,a,b,c]
        '''
        return 0

class User:

    def __init__(self, name):
        self.name = name
        self.random = -1 
        self.subkey = -1
        self.key = -1

    # Una vez se tiene el mensaje que envia el KGC, se recupera la clave.
    def generateRandom(self):
        self.random = getrandbits(64)
        return self.random
    def recoverKey(self, msg):
        #TODO
        
        return self.key

## Test zone

kgc = KeyGenerationCenter(8)

users = []
for n in range(8):
    users.append(User("Name"+str(n)))

kgc.recibeUsuarios(users)
kgc.recibeRandoms()
kgc.generateSubKeys()
print(kgc.key)
print(kgc.users)
print(kgc.subkeys)
print(kgc.randoms)

for n in users:
    print(n.random)

print(calculaClave(kgc.key))




