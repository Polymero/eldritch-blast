#!/usr/bin/env python3
#
# Polymero
#

# Imports
import socket
import os, sys
import random
import json, pickle


def getIP():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.settimeout(0)
	try:
		s.connect(('10.254.254.254', 1))
		ip = s.getsockname()[0]
	except:
		ip = '127.0.0.1'
	s.close()
	return ip


if len(sys.argv) < 2:
	print('Missing some inputs here.... Hello?')
	exit()


if sys.argv[1] in ['-h', '--host']:

	HOST = 1

	recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try: recv_socket.bind(('', int(sys.argv[2])))
	except: recv_socket.bind(('', 12000))

	recv_socket.listen()
	print('Hosting on', getIP(), recv_socket.getsockname()[1])
	print('Waiting for other player to connect...')

	connection, address = recv_socket.accept()

	print('Player connected from', address)


if sys.argv[1] in ['-j', '--join']:

	HOST = 0

	connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try: connection.connect((sys.argv[2], int(sys.argv[3])))
	except: print('Failed to join game...'); exit()

	print('Joined game at', connection.getpeername())


#--------------------
# GAME LOOP
#--------------------

BOARD = """
 {} | {} | {}
---+---+---
 {} | {} | {} 
---+---+---
 {} | {} | {}
"""

class GAME:
	def __init__(self):
		self.state = 9 * [' ']

	def __getstate__(self):
		return self.__dict__
	
	def __setstate__(self, objdict):
		self.__dict__ = objdict

game = GAME()

if HOST:
	PLAYER = 'X'
else:
	PLAYER = 'O'

print('You are "{}":'.format(PLAYER))
print(BOARD.format(*game.state))

if HOST:

	move = input('Move? (1-9) ')
	game.state[int(move)] = PLAYER
	connection.send(pickle.dumps(game))

else:

	print('Waiting for host to make move...')

while True:

	game = pickle.loads(connection.recv(1024))
	print(BOARD.format(*game.state))

	move = input('Move? (1-9) ')
	game.state[int(move) - 1] = PLAYER
	connection.send(pickle.dumps(game))

	print(BOARD.format(*game.state))









# class Game:
# 	def __init__(self):
# 		self.hand = list(range(24))
# 		random.shuffle(self.hand)
		

# 	def __getstate__(self):
# 		return self.__dict__

# 	def __setstate__(self, game_dict):
# 		self.__dict__ = game_dict


# if HOST:

# 	game = Game()

# 	connection.send(pickle.dumps(game))


# for _ in range(10):

# 	game = pickle.loads(connection.recv(1024))

# 	print('<', game.hand)

# 	random.shuffle(game.hand)

# 	print('>', game.hand)

# 	connection.send(pickle.dumps(game))



