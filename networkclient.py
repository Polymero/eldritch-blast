#!/usr/bin/env python3
#
# Polymero
#

# Imports
from socket import *
import os, sys
import random
import json, pickle


if len(sys.argv) < 2:
	print('Missing some inputs here.... Hello?')
	exit()


if sys.argv[1] in ['-h', '--host']:

	HOST = 1

	recv_socket = socket(AF_INET, SOCK_STREAM)

	try: recv_socket.bind(('', int(sys.argv[2])))
	except: recv_socket.bind(('', 12000))

	recv_socket.listen()
	print('Hosting on PORT', recv_socket.getsockname()[1])
	print('Waiting for other player to connect...')

	connection, address = recv_socket.accept()

	print('Player connected from', address)


if sys.argv[1] in ['-j', '--join']:

	HOST = 0

	connection = socket(AF_INET, SOCK_STREAM)

	try: connection.connect((sys.argv[2], int(sys.argv[3])))
	except: print('Failed to join game...'); exit()

	print('Joined game at', connection.getpeername())


class Game:
	def __init__(self):
		self.hand = list(range(24))
		random.shuffle(self.hand)
		

	def __getstate__(self):
		return self.__dict__

	def __setstate__(self, game_dict):
		self.__dict__ = game_dict


if HOST:

	game = Game()

	connection.send(pickle.dumps(game))


for _ in range(10):

	game = pickle.loads(connection.recv(1024))

	print('<', game.hand)

	random.shuffle(game.hand)

	print('>', game.hand)

	connection.send(pickle.dumps(game))



