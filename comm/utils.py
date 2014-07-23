
from hashlib import sha1
# Parametros en comun, grupo generador, etc
GENERATOR = 2
#MODULUS   = getrandbits(1024)
#MODULUS   = 156431412343
def join(st):
    rs = ""
    for n in st:
        rs += n
    return rs
#MODULUSOLD =19550235927307083440054695612358531084944020582733423559498026006885889846837203202394738273571323894323128697432887000133230027946925224117548714912282882284936474903101894318334954325904200515232369013007948470835560263267168474167123159156978856947906463414127870757350416082973157138057134576785904471413L 

MODP = """FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1\
          29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD\
          EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245\
          E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED\
          EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D\
          C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F\
          83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D\
          670C354E 4ABC9804 F1746C08 CA237327 FFFFFFFF FFFFFFFF"""
MODULUS = int(join(MODP.split()),16)
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
def keyRecover(gs1,gs2r,gr,mod):
    r = gs1*gs2r%mod
    return r * modInverse(gr,mod)%mod


