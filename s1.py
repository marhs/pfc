# Tcp Chat server
 
import socket, select
import kgc
state = 0 
participants = []

PORT = 5000

#######
k = kgc.KeyGenerationCenter(128,2)

#######
# Hace BROADCAST de un mensaje a todos los sockets activos. 
def broadcast_data (message):
    global state
    message = str(state)+':server:'+message
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
def processData(data):

    global state

    print '   Analizing data', data
    d = data.split(':')
    if len(d)!=3:
        return False

    if d[0] == '0':
        print '    Adding participant '+str(d[0])
        participants.append(d[1])
        if k.addUser(d[1]) == 1:
            print 'Usuarios k: ',k.users

        if len(participants) == 2 and state == 0:
            broadcast_data(str(participants))
            state += 1
            return True

    elif d[0] == '1':
        print('Estado 1')


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
                    processData(data)
          
                #In Windows, sometimes when a TCP program closes abruptly,
                # a "Connection reset by peer" exception will be thrown
             
            except:
                broadcast_data("Client (%s, %s) is offline" % addr)
                # TODO Fin de la conexion, cliente desconectado. 
                print "Client (%s, %s) is offline" % addr
                sock.close()
                CONNECTION_LIST.remove(sock)
                continue
 
server_socket.close()
