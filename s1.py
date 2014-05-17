# Tcp Chat server
 
import socket, select, sys
import kgc

import json
state = 0 
participants = []

PORT = int(sys.argv[1])

#######
k = kgc.KeyGenerationCenter(128,2)
#######


def broadcast_data (message):
# Hace BROADCAST de un mensaje a todos los sockets activos. 
    # TODO Enviar en json y recibir en json
    global state
    print '[',state,'] SENT:', message 
    message = str(k.state)+':server:'+json.dumps(message)
    for socket in CONNECTION_LIST:
        if socket != server_socket:
            try :
                socket.send(message)
            except :
                # Si ha fallado el socket.send() es que el socket no esta activo, por lo
                # tanto habria que parar el protocolo. TODO 
                socket.close()
                CONNECTION_LIST.remove(socket)


# Tratamiento de datos recibidos. 
def processData(sock,data):
    global state
    print '[',state,'] RECV:', data  
    d = data.split(':',2)
    if len(d)!=3:
        return False

    # Estado 0: Capturar los participantes. 
    # Lo dejamos para bingo
    if d[0] == '0' or d[0] == '1':
        # Pueden llegar dos posibles respuestas: El nombre y el ACK

        # Llega el nombre - addUser
        if d[0] == '0':
            print '    Adding participant '+str(d[2])
            state = k.addUser(d[1]) # TODO Que hace esto? Mejor/que devuelve?
            # Entonces envia la clave
            msg_sent = '0:server:'+str(k.subkeys[d[1]])
            print '[',state,'] SENT:', msg_sent  
            sock.send(msg_sent)

        # Llega la clave - userRdy
        else:
            if d[2] != 'ACK':
                print 'ERROR, DATO 2 != ACK'
            else:
                state = k.userRdy()

        # Si todos los usuarios han enviado el ACK, se envia la lista de users
        if state == 1:
            msg_sent = k.getData()
            broadcast_data(msg_sent)
            #k.resetUserRdy()
            return True


    elif d[0] == '2':
        # Estado 1, recibe los randoms, los almacena y cuando los tiene todos los envia
        k.resetUserRdy()

        state = k.recibeRandom(d[1],int(d[2])) 
        if state == 2:
            broadcast_data(k.getData())

    elif d[0] == '3':
        # Recibe los ACK de todos los participantes y envia el M,Auth
        print '    ',d
        if d[2] == 'ACK':
            state = k.userRdy()
        if state == 3:
            msg = k.getData()
            broadcast_data(msg)


    elif d[0] == '4':
        print 'Datos recibidos 4'
        #print k.generateHi()
        print d[2] == k.generateHi(d[1])
    return True


     
# List to keep track of socket descriptors
CONNECTION_LIST = []
RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", PORT))
server_socket.listen(20)

# Add server socket to the list of readable connections
CONNECTION_LIST.append(server_socket)

print "Server started on port " + str(PORT)

while 1:
    # Get the list sockets which are ready to be read through select
    read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
    for sock in read_sockets:
        #New connection
        if sock == server_socket:
            # Handle the case in which there is a new connection recieved through server_socket
            sockfd, addr = server_socket.accept()
            CONNECTION_LIST.append(sockfd)
            print "Client (%s, %s) connected" % addr
             
         
        #Some incoming message from a client
        else:
            # Data recieved from client, process it
            try:

                data = sock.recv(RECV_BUFFER)
                if data:
                    processData(sock,data)
          
                #In Windows, sometimes when a TCP program closes abruptly,
                # a "Connection reset by peer" exception will be thrown
             
            except:
                # TODO Fin de la conexion, cliente desconectado. 
                print "Client (%s, %s) is offline" % addr
                sock.close()
                CONNECTION_LIST.remove(sock)
                continue
 
server_socket.close()
