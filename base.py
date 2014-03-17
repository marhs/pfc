# Protocolo de comparticion de claves

# SystemRandom usa el generador de numeros aleatorios del sistema
# /dev/urandom
# es una clase envoltura de os.urandom
from random import SystemRandom
from random import getrandbits

class KeyGenerationCenter:

    def __init__(self, keySize):
        self.keySize = keySize
        self.key = self.generateKey(keySize)
        self.users = dict()
        self.active = 0

    def sendUsers(self):
        print(list(self.users.keys()))

    def generateKey(self, keySize):

        return getrandbits(self.keySize)

    def generateSubKeys(self, users):
        
        for client in users:
            self.users[client] = self.generateSubKey()

        return self.users

    def generateSubKey(self):

        subkey = getrandbits(self.keySize)
        while subkey > self.key:
            subkey = getrandbits(self.keySize)

        return subkey

class User:

    def __init__(self, name):
        self.name = name
        self.key = -1

        
    def recoverKey(self, msg):
        #TODO
        
        return self.key

## Test zone

kgc = KeyGenerationCenter(8)


users = []
for n in range(8):
    users.append(User("Name"+str(n)).name)

kgc.generateSubKeys(users)
print(kgc.key)
print(kgc.users)
kgc.sendUsers()




