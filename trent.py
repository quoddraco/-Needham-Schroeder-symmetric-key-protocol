import socket
import random
import pyaes
import string

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
IP = socket.gethostbyname(socket.gethostname())
PORT = 12335
listener.bind((IP, PORT))
listener.listen(0)
connection, address = listener.accept()

key_A="evangelion_evangelion_evangelion"# ключ клиента А
key_A= key_A.encode('utf-8')
key_B="confidence-confidence-confidence"# ключ клиента В
key_B= key_B.encode('utf-8')
K=""

def generate_random_session_key():# функция по генерации сессионного ключа
    length=32# длина ключа
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string


def client_A():
     while True:# слушаем клиента
         data = connection.recv(1024).decode('utf-8')
         if (data != ''):
             break
     print("Сообщение от клиента_А: [",data,"]")
     data=data.split(":")
     name_A=data[0]# имя клиента А
     name_B=data[1]# имя клиентов В
     r_A=data[2]# случайное число клиента А
     print("Имя клиента_А:",name_A)
     print("Имя клиента_В:",name_B)
     print("Случайное число клиента_А:",r_A)

     K=generate_random_session_key()#сессонный ключ
     print("Сгенирированный сессионный ключ:",K)
     aes = pyaes.AESModeOfOperationCTR(key_B)
     message_to_be_client_B = aes.encrypt("{}:{}".format(K,name_A))# шифруем сообщение кленту B по его ключу
     print("Зашифрованное сообщение для клиента_В:",message_to_be_client_B)
     connection.send(message_to_be_client_B)# отправляем сообщение клиенту А

     aes = pyaes.AESModeOfOperationCTR(key_A)# шифруем сообщение кленту А по его ключу
     message_to_be_client_A = aes.encrypt("{}:{}:{}:{}".format(r_A, name_B, K,message_to_be_client_B))
     print("Зашифрованное сообщение для клиента_A:",message_to_be_client_A)
     connection.send(message_to_be_client_A)# отправляем сообщение клиенту А


#Начало программы
print("=============Trent=============")
client_A()
print("==================================")
