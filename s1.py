# Tcp Chat server
 
import socket, select, sys
import kgc
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
    message = str(k.state)+':server:'+str(message)
    for socket in CONNECTION_LIST:
        if socket != server_socket:
            try :
                socket.send(str(message))
            except :
                # Si ha fallado el socket.send() es que el socket no esta activo, por lo
                # tanto habria que parar el protocolo. TODO 
                socket.close()
                CONNECTION_LIST.remove(socket)


# Tratamiento de datos recibidos. 
def processData(sock,data):
    global state
    print '   Analizing data', data
    d = data.split(':')
    if len(d)!=3:
        return False

    # Estado 0: Capturar los participantes. 
    # TODO: Aqui es donde deberia enviar POR SEPARADO la subclave. 
    # Lo dejamos para bingo
    if d[0] == '0':
        print '    Adding participant '+str(d[2])
        state = k.addUser(d[1]) 
        sock.send('-1:server:'+str(k.subkeys[d[1]]))
        if state == 1:
            print 'Usuarios k: ',k.users
            print k.getData()
            broadcast_data(k.getData())
            return True

    elif d[0] == '1':
        # Estado 1, recibe los randoms, los almacena y cuando los tiene todos los envia

        print d
        state = k.recibeRandom(d[1],int(d[2])) 
        if state == 2:
            print '    Random completados'
            print k.getData()
            broadcast_data(k.getData())

    elif d[0] == '2':
        # Recibe los ACK de todos los participantes y envia el M,Auth
        print d
        if d[2] == 'rdy':
            state = k.userRdy()
        if state == 3:
            print 'Ship rdy, pal'
            msg = k.getData()
            print msg
            broadcast_data(msg)
        

    return True


     
# List to keep track of socket descriptors
CONNECTION_LIST = []
RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
 
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", PORT))
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
