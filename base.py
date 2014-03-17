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

    def generateSubKey(self):

        subkey = getrandbits(self.keySize)
        while subkey > self.key:
            subkey = getrandbits(self.keySize)

        return subkey
## Test zone

kgc = KeyGenerationCenter(8)

users = ['user1','user2']
kgc.generateSubKeys(users)
print(kgc.key)
print(kgc.users)
kgc.sendUsers()


