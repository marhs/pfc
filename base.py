# Protocolo de comparticion de claves

# SystemRandom usa el generador de numeros aleatorios del sistema
# /dev/urandom
# es una clase envoltura de os.urandom



## Test zone

"""
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
"""
    






