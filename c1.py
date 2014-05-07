# telnet program example
import socket, select, string, sys
state = 0 

#main function

host = 'localhost'    
port = 5000
myData = ['helmetk','123123141']
name = 'helmetk'
rand = 1231151
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(20)
 
def send0(s,msg):
    global state
    msg = str(state) + ':' + name+':'+ str(msg)
    print 'MSG SENT: ',msg
    s.send(msg)
    return 0

def analizeData(s,msg):
    global state
    msg_data = msg.split(':') # TODO Split(':',2)o
    if state > 1:
        print 'State > 1'
        return True
    if state == 0 or state == int(msg[0]):
        # DO ACTIONS
        send0(s,myData[state])
        state += 1
    return 0
# connect to remote host
try :
    s.connect((host, port))
except :
    print 'Unable to connect'
    sys.exit()

## SEND THE FIRST MESSAGE
analizeData(s,name)
 

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
                analizeData(s,data)
                
         
        #user entered a message
  

