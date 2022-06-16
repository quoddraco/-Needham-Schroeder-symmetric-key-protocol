import socket
import random
import pyaes

my_name="Bob"# имя клиента В
name_A="Alice"# имя клиента А
key_B="confidence-confidence-confidence"
key_B= key_B.encode('utf-8')# ключ шифрования
K=""

def client_A():# функция по работе с клиентом А
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 12334
    listener.bind((IP, PORT))
    listener.listen(0)
    connection, address = listener.accept()
    while True:# получаем сообщение клиента А (от трента)
        data = connection.recv(1024)
        if (data != ''):
            break
    aes = pyaes.AESModeOfOperationCTR(key_B)
    decrypted_message_from_client_A = aes.decrypt(data).decode('utf-8')# расшифровываем сообщение (по собственному ключу)
    print("Сообщение от клиента_А: [",decrypted_message_from_client_A,"]")
    data=decrypted_message_from_client_A.split(":")
    print("Cессионный ключ:", data[0])
    K=data[0]# Cессионный ключ
    K = K.encode('utf-8')
    if data[1]==name_A:# проверка на отклик
        print("Сообщение подтверждено!")
        r_B = random.getrandbits(64)
        print("Cлучайное число R_B:", r_B)

        aes = pyaes.AESModeOfOperationCTR(K)# шифруем сообщение кленту А по сессионному ключу
        message_to_be_client_A = aes.encrypt(str(r_B))
        connection.send(message_to_be_client_A)# отправляем сообщение клиенту А (R_В)

        while True:# получаем сообщение клиента А
            data = connection.recv(1024)
            if (data != ''):
                break

        aes = pyaes.AESModeOfOperationCTR(K)# расшифровываем сообщение (по сессионному ключу)
        decrypted_message_from_client_A = aes.decrypt(data).decode('utf-8')
        mess= int(decrypted_message_from_client_A)

        if (r_B-1)==mess:# проверка
            print("Успех!")
            mess="Успех!"
            connection.send(mess.encode('utf-8'))
        else:
            print("Failed!")
            mess = "Failed!"
            connection.send(mess.encode('utf-8'))

    else:
        print("Failed!")


#Начало программы
print("=============Клиент_В=============")
client_A()
print("==================================")
