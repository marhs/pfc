import socket
import json

# Se envian datos en forma de diccionario
def sendData(datos):
    
    data_string = json.dumps(data)    
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost',30000))
    s.send(str.encode(data_string, 'utf-8'))

def receiveData()
    # TODO

    return 0
# TODO Excepciones a todo, comprobar que se envia bien. 

