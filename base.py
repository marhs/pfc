# Protocolo de comparticion de claves



# SystemRandom usa el generador de numeros aleatorios del sistema
# /dev/urandom
# es una clase envoltura de os.urandom
from random import SystemRandom
from random import getrandbits

SIZE_KEY = 1024

# Generacion de la clave secreta S

def generateGroupKey(secret):
    
    return getrandbits(SIZE_KEY)


# Division de S en n subclaves.

def generateSubKeys(key):
    for n in range(10):
        subkey = getrandbits(SIZE_KEY)
        while subkey > key:
            print("Regenerating")
            subkey = getrandbits(SIZE_KEY)

        print(key, " = ", subkey, ' + ', key-subkey)
    
    return 0

## Test zone

key = generateGroupKey(1)
generateSubKeys(key)


