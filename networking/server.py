import socket
import threading
import pickle

from backend.game_status import GameStatus
from backend.player import Player
from backend.game import Game
from time import sleep


class Server:
    HEADER = 4096
    PORT = 5050
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDRESS = (SERVER, PORT)
    FORMAT = 'utf-8'
    DISCONNECT_MESSAGE = "!DISCONNECT"
    WAITING_TIME = 60

    def __init__(self, game):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDRESS)
        self.game = game
        self.active_clients = dict()
        self.timer = 0

    def update_all_clients(self):
        for (connection, address) in self.active_clients.keys():
            game_state = pickle.dumps(self.game)
            message_size = len(game_state)
            send_length = str(message_size).encode(self.FORMAT)
            send_length += b' ' * (self.HEADER - len(send_length))
            connection.send(send_length)
            connection.send(game_state)

    def handle_client(self, connection, address):
        print(f"[NEW CONNECTION] {address} connected")
        self.active_clients[(connection, address)] = None
        message_length = connection.recv(self.HEADER).decode(self.FORMAT)
        if message_length:
            message_length = int(message_length)
            player_name = pickle.loads(connection.recv(message_length))
            self.active_clients[(connection, address)] = Player(player_name, Player.STARTING_FUNDS)
            self.game.players.add_player(self.active_clients[(connection, address)])
            self.update_all_clients()

        connected = True
        while connected:
            message_length = connection.recv(self.HEADER).decode(self.FORMAT)
            if message_length:
                message_length = int(message_length)
                message = pickle.loads(connection.recv(message_length))

                if message == self.DISCONNECT_MESSAGE:
                    connected = False

                print(f"[{address}] {message}")
                self.game.handle_action(self.active_clients[(connection, address)], message)
                self.game.print_game_info()
                self.update_all_clients()

        self.active_clients.pop((connection, address))
        connection.close()

    def track_waiting(self):
        while self.timer < self.WAITING_TIME or self.game.players.number_of_players < 2:
            sleep(1)
            self.timer += 1
        if self.game.status < GameStatus.PREFLOP:
            self.game.change_game_status()
            self.update_all_clients()
            print("Game started!")
            self.game.print_game_info()

    def start(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        counter = None
        while True:
            connection, address = self.server.accept()
            if self.timer > self.WAITING_TIME:
                break
            else:
                if counter is not None:
                    counter.join(timeout=0)
                self.timer = 0
                counter = threading.Thread(target=self.track_waiting)
                counter.start()
            thread = threading.Thread(target=self.handle_client, args=(connection, address))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {len(self.active_clients.keys()) + 1}")


if __name__ == "__main__":
    game = Game([])
    game.print_game_info()
    server = Server(game)
    server.start()
