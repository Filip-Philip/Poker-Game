import socket
import threading
import pickle


class Server:
    HEADER = 64  # may be too small
    PORT = 5050
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDRESS = (SERVER, PORT)
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "!DISCONNECT"

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDRESS)

    def handle_client(self, connection, address):
        print(f"[NEW CONNECTION] {address} connected")

        connected = True
        while connected:
            message_length = connection.recv(self.HEADER).decode(self.FORMAT)
            if message_length:
                message_length = int(message_length)
                message = connection.recv(message_length).decode(self.FORMAT)
                if message == self.DISCONNECT_MESSAGE:
                    connected = False

                print(f"[{address}] {message}")
                connection.send("Message received".encode(self.FORMAT))

        connection.close()

    def start(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        while True:
            connection, address = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(connection, address))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
