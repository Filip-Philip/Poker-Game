import socket
import pickle
from backend.PlayerAction import PlayerAction
from backend.Game import Game
import threading
import sys


class Client:
    HEADER = 4096
    PORT = 5050
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "!DISCONNECT"
    # SERVER = "LOCAL IP OF SERVER"
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDRESS = (SERVER, PORT)

    def __init__(self, player_id):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDRESS)
        self.player_id = player_id

    def send(self, msg):
        message = pickle.dumps(msg)
        message_length = len(message)
        send_length = str(message_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        # print(self.client.recv(2048).decode(self.FORMAT))

    def receive(self, connection, address):
        connected = True
        while connected:
            message_length = connection.recv(self.HEADER).decode(self.FORMAT)
            if message_length:
                message_length = int(message_length)
                message = pickle.loads(connection.recv(message_length))
                if message == self.DISCONNECT_MESSAGE:
                    connected = False

                # if type(message) == Game:
                message.print_game_info()
                print(f"[{address}] {message}")
                # connection.send("Message received".encode(self.FORMAT))

    def start(self):
        print(f"[LISTENING] Client is listening on {self.client}")
        thread = threading.Thread(target=self.receive, args=(self.client, self.ADDRESS))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__":
    player_nickname = sys.argv[1]
    client = Client(player_nickname)
    client.send(player_nickname)
    client.start()
    action = None
    while action != "q":
        action = input("Action: ")
        if action == "raise":
            client.send(PlayerAction.RAISE)
        elif action == "fold":
            client.send(PlayerAction.FOLD)
        elif action == "check":
            client.send(PlayerAction.CHECK)
        elif action == "call":
            client.send(PlayerAction.CALL)

    client.send(client.DISCONNECT_MESSAGE)