# telnet program example
import socket, select, string, sys
import user
import json
state = 0 


## CAREFUL HERE BE DRAGONS
# TODO Anadir excepciones para el sys.argv
u = user.User(sys.argv[1])
#main function

host = 'localhost'    
port = int(sys.argv[2])
myData = ['helmetk','123123141']
rand = 1231151
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(20)
 
def send0(s,msg):
    global state
    msg = str(state) + ':' + u.name+':'+ str(msg)
    print 'MSG SENT: ',msg
    s.send(msg)
    return 0

def processData(s,msg):
    print 'processingData(',msg
    global state
    msg_data = msg.split(':') # TODO Split(':',2)o
    state = int(msg_data[0])
    print 'State =',state
    if state == 0 :
        # DO ACTIONS
        send0(s,u.getData())
        state += 1
    elif state == 1:
        send0(s,u.getData())
        state = msg_data[0]
        print state
    elif state > 2:
        return True
    elif state == 2:
        send0(s,'rdy')
        print 'Estado 2'
    elif state == -1:
        u.subkey = msg_data[2]
    return 0
# connect to remote host
try :
    s.connect((host, port))
except :
    print 'Unable to connect'
    sys.exit()

## SEND THE FIRST MESSAGE
processData(s,'0:'+u.name+':'+u.name)
 

## BUCLE DE ESPERA 
while 1:
    socket_list = [s]
    print 'Esperando respuesta del servidor en estado ' +str(state) 
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
                print 'Data received: ', data
                processData(s,data)
                
         
        #user entered a message
  

