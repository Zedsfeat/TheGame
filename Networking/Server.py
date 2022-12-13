import os
import random
import socket
import threading

host = '127.0.0.1'
port = 5060

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
list_num = dict()


class Player:
    counter = 0

    def __init__(self, nickname, client: socket):
        self.nickname = nickname
        Player.counter += 1
        self.id = Player.counter
        self.client: socket = client
        self.game = None

    def set_game(self, game):
        self.game: Game = game

    def remove_game(self):
        self.game.remove_player(self)
        self.game = None

    def __str__(self):
        return self.id.__str__() + " - " + self.nickname


class Game:
    counter = 0

    def __init__(self, player: Player):
        self.creator: Player = player
        Game.counter += 1
        self.id = Game.counter
        self.players = [player]
        self.step_counter = random.choice([0, 1])

    def set_player(self, player: Player):
        if len(self.players) >= 2:
            raise RuntimeError()
        self.players += [player]
        if self.players == 2:
            game_broadcast(self, '')

    def remove_player(self, player):
        if player in self.players:
            self.players.pop(self.players.index(player))
        if len(self.players) == 0:
            games.pop(self.id)

    def __str__(self):
        return f"{self.id}: {self.creator.nickname}"


games = {}
players = {}


def dict_string(some_dict):
    result = ""
    for key, value in some_dict.items():
        result += value.__str__() + "\n"
    return result


def game_broadcast(game: Game, message):
    counter = 0
    step_on = "true"
    step_off = "false"
    for player in game.players:
        if counter == game.step_counter:
            player.client.send(step_on.encode('ascii'))
        else:
            player.client.send(step_off.encode('ascii'))
        player.client.send(message.encode('ascii'))
        counter += 1
    game.step_counter = (game.step_counter + 1) % 2


# def broadcast(game: Game, message):
#     for player in game.players:
#         player.client.send(message.encode('ascii'))

def handle2(player: Player):

    while True:
        try:
            message = player.client.recv(1024).decode('ascii')
            # game_broadcast(player.game, message)
            print(message)
        except:
            # game = player.game
            # game.remove_player(player)
            # game_broadcast(game, "Wait for new opponent...")
            # players.pop(player.id)
            break

def handle(player: Player):

    req = -1
    player.client.send("1. Create Game\n"
                       "2. Join the Game".encode('ascii'))
    while req not in [1, 2]:
        try:
            req = int(player.client.recv(1024).decode('ascii').split()[1])
        except ValueError:
            req = -1
            player.client.send("1. Create Game\n"
                               "2. Join the Game".encode('ascii'))
    if req == 1:
        game = Game(player)
        player.set_game(game)
        games[game.id] = game
        print(f"Game {game} was created")
        player.client.send("Wait for opponent...".encode('ascii'))
    else:
        game_chosen_id = -1
        free_games = {k: v for k, v in games.items() if len(v.players) == 1}
        while game_chosen_id not in free_games.keys():
            player.client.send(dict_string(free_games).encode('ascii'))
            try:
                game_chosen_id = int(player.client.recv(1024).decode('ascii').split()[1])
                games[game_chosen_id].set_player(player)
                player.set_game(games[game_chosen_id])
            except Exception:
                game_chosen_id = -1
                free_games = {k: v for k, v in games.items() if len(v.players) == 1}
    while True:
        try:
            message = player.client.recv(1024).decode('ascii')
            game_broadcast(player.game, message)
        except:
            game = player.game
            game.remove_player(player)
            game_broadcast(game, "Wait for new opponent...")
            players.pop(player.id)
            break


def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Запрос и получение никнейма
        nickname = client.recv(1024).decode('ascii')

        # Создание игрока
        player = Player(nickname, client)
        players[player.id] = player



        print("PLayer " + player.__str__() + " was created!")

        handle2(player)
        thread = threading.Thread(target=handle2, args=(player,))
        thread.start()

receive()

