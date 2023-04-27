import socket
import threading

HOST = '127.0.0.1'
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
# Vai ser um serve que vai ficar escutando
server.listen()

salas = {}

def broadcast(sala, message):
    for i in salas[sala]:
        if isinstance(message, str):
            message = message.encode()

        i.send(message)


def send_message(nome, sala, client):
    while True:
        message = client.recv(1024)
        message = f'{nome}: {message.decode()}\n'
        broadcast(sala, message)


while True:
    # Conexão do user com o server
    client, addr = server.accept()
    client.send(b'SALA')
    sala = client.recv(1024).decode()
    nome = client.recv(1024).decode()
    
    if sala not in salas.keys():
        salas[sala] = []
    salas[sala].append(client)
    print(f'{nome} se conectou na sala {sala}! INFO {addr}')
    broadcast(sala, f'{nome}: Entrou na sala\n')
    thread = threading.Thread(target=send_message, args=[nome, sala, client])
    thread.start()