
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

    # TODO

    return [1,2,3,4]
