
from hashlib import sha1

# TODO Cambiar esto a utilidades.py
def calculaClave(secret,generator,modulus):
    return pow(generator, secret, modulus)

def resumen(parametros):
    res = sha1()
    res.update(mensaje)

def encoder(element):
    return str(element).encode()

def hs(listaElementos):
    res = sha1()
    for element in listaElementos:
        res.update(encoder(element))

    return res.hexdigest()


def mostrarMensaje(mensaje):
    for msg in mensaje:
        print(msg)

def extEuclides(a,b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return [gcd, x, y]

def modInverse(a,b):
    eu = extEuclides(a,b)
    return eu[1]%b

# Equivalente a resolver la ecuacion clave que devuelve K'
def despejarClave(gs1,gs2r,gr,mod):
    r = gs1*gs2r%mod
    return r * modInverse(gr,mod)%mod
