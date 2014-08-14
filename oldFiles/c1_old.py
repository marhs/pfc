# Tcp client

# Llamada c1.py nombre puerto
import socket, select, string, sys
import user
import json
state = 0 


## CAREFUL HERE BE DRAGONS
# TODO Anadir excepciones para el sys.argv
u = user.User(sys.argv[1])

host = 'localhost'    
port = int(sys.argv[2])
myData = ['helmetk','123123141']
rand = 1231151
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(20)
 
def send0(s,msg):
    global state
    msg = str(state) + ':' + u.name+':'+ str(msg)
    print '[',state,'] SENT:', msg  
    s.send(msg)
    return 0

def processData(s,msg):
    if msg == '': #Dato vacio, mensaje inicial. 
        send0(s,u.getData())
        return 0

    global state
    msg_data = msg.split(':',2) # TODO Split(':',2)o
    state = int(msg_data[0])
    print '[',state,'] RECV:', msg_data  

    if state == 0 :
        # Recibe subclave y envia ACK 0/1
        # TODO json.loads carga un long en la subkey, ver si eso reporta problemas
        u.subkey = json.loads(msg_data[2])
        state += 1
        send0(s,u.getData())
    elif state == 1:
        # Recibe users y envia el random
        # TODO json.loads carga aqui un unicode en vez de un string, puede dar
        #      problemas tambien pero u'abc' == 'abc, asi que veremos a ver
        u.users = json.loads(msg_data[2])
        state += 1
        send0(s,u.getData())
    elif state == 2:
        # Recibe randoms[] y envia ACK
        u.publicRandoms = json.loads(msg_data[2])
        state += 1
        #send0(s,'ACK')
        send0(s,u.getData())
    elif state == 3:
        # Recibe el MAuth, genera el H, K y hi
        hlocal = u.recoverMsg(json.loads(msg_data[2]))
        if u.genH() == hlocal[2]:
            print 'ALL OK'
        else: 
            # TODO Fallo del algoritmo, no se ha comprobado envia FAIL y vuelve
            print 'FAIL'
            return 0
        u.recoverKey()
        u.generateAuth()
        u.computeHi()

        state += 1
        send0(s,u.getData())
        return 0
    elif state == 5:
        u.finish() 
        # FINISH SEQ
    elif state > 2:
        return True
# connect to remote host
try :
    s.connect((host, port))
except :
    print 'Unable to connect'
    sys.exit()

## SEND THE FIRST MESSAGE
processData(s,'')
 

## BUCLE DE ESPERA 
while 1:
    socket_list = [s]
    #print 'Esperando respuesta del servidor en estado ' +str(state) 
    # Get the list sockets which are readable
    read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
     
    for sock in read_sockets:
        #incoming message from remote server
        if sock == s:
            data = sock.recv(4096)
            if not data :
                print '\nDisconnected from chat server'
                sys.exit()
            else :
                # Ha recibido datos
                # Comprobar el estado, si todo va bien, enviar el siguiente estado
                processData(s,data)
                
         
        #user entered a message
  

