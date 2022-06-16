import socket
import random
import pyaes

my_name="Alice"# имя клиента А
name_B="Bob"# имя клиента В
r_A=random.getrandbits(64)# случайное число (идентификатор)
key_A="evangelion_evangelion_evangelion"# ключ шифрования
key_A= key_A.encode('utf-8')

def trent():# функция по работе с "трентом"
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP = "192.168.56.1"
    PORT = 12335
    connection.connect((IP, PORT))# подключаемся к тренту (серверу)

    print("Cлучайное число R_A:",r_A)
    message="{}:{}:{}".format(my_name,name_B,r_A)
    connection.send(message.encode('utf-8'))# отправляем тренту имена и случ. число

    while True:# получаем сообщение от трента(сообщение для клиента В)
        data_B = connection.recv(1024)
        if (data_B != ''):
            break
    while True:# получаем сообщение от трента
        data = connection.recv(1024)
        if (data != ''):
            break

    aes = pyaes.AESModeOfOperationCTR(key_A)
    decrypted_message_from_trent = aes.decrypt(data).decode('utf-8')# расшифровываем сообщение (по собственному ключу)
    print("Сообщение от trent: [",decrypted_message_from_trent,"]")
    data=decrypted_message_from_trent.split(":")
    if int(data[0])==r_A and data[1]==name_B:# проверка на отклик
        print("Сообщение подтверждено!")
        print("Cессионный ключ:",data[2])
        client_B(data[2],data_B)
    else:
        print("Failed!")

def client_B(K,data_B):# функция по работе с клиентом В
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP = "192.168.56.1"
    PORT = 12334
    connection.connect((IP, PORT))# подключаемся к клиенту (серверу)
    connection.send(data_B)# отправляем сообщение клиенту В (от трента)

    while True:# принимаем сообщение от клиента В
        data = connection.recv(1024)
        if (data != ''):
            break

    K = K.encode('utf-8')
    aes = pyaes.AESModeOfOperationCTR(K)
    decrypted_message_from_client_B = aes.decrypt(data).decode('utf-8')# расшифровываем сообщение (по сессионному ключу)
    print("Сообщение от клиента_B: [", decrypted_message_from_client_B, "]")
    r_B = int(decrypted_message_from_client_B)
    print("Случайное число клиента_В:",r_B)

    aes = pyaes.AESModeOfOperationCTR(K)
    message_to_be_client_B = aes.encrypt(str(r_B-1))# шифруем сообщение кленту B по сессионному ключу
    connection.send(message_to_be_client_B)# отправляем сообщение клиенту В (R_В - 1)

    while True:# слушаем клиента В
        data = connection.recv(1024).decode('utf-8')
        if (data != ''):
            break
    print(data)


#Начало программы
print("=============Клиент_A=============")
trent()
print("==================================")