#!/usr/bin/env python3
#
# Polymero
#

# Imports
import socket
import os, sys, time
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

# BOARD = """
#     1   2   3   4   5   6   7   8   9
#   +---+---+---+---+---+---+---+---+---+
# A | {}   {}   {}   {}   {}   {}   {}   {}   {} |
#   +   +   +   +   +   +   +   +   +   +
# B | {}   {}   {}   {}   {}   {}   {}   {}   {} |
#   +   +   +   +   +   +   +   +   +   +
# C | {}   {}   {}   {}   {}   {}   {}   {}   {} |
#   +   +   +   +   +   +   +   +   +   +
# D | {}   {}   {}   {}   {}   {}   {}   {}   {} |
#   +   +   +   +   +   +   +   +   +   +
# E | {}   {}   {}   {}   {}   {}   {}   {}   {} |
#   +   +   +   +   +   +   +   +   +   +
# F | {}   {}   {}   {}   {}   {}   {}   {}   {} |
#   +   +   +   +   +   +   +   +   +   +
# G | {}   {}   {}   {}   {}   {}   {}   {}   {} |
#   +   +   +   +   +   +   +   +   +   +
# H | {}   {}   {}   {}   {}   {}   {}   {}   {} |
#   +   +   +   +   +   +   +   +   +   +
# I | {}   {}   {}   {}   {}   {}   {}   {}   {} |
#   +---+---+---+---+---+---+---+---+---+
# """

BOARD = """
    1   2   3   4   5   6   7   8   9
  +-----------------------------------+
A | {}   {}   {}   {}   {}   {}   {}   {}   {} |
  |   +   +   +   +   +   +   +   +   |
B | {}   {}   {}   {}   {}   {}   {}   {}   {} |
  |   +   +   +   +   +   +   +   +   |
C | {}   {}   {}   {}   {}   {}   {}   {}   {} |
  |   +   +   +   +   +   +   +   +   |
D | {}   {}   {}   {}   {}   {}   {}   {}   {} |
  |   +   +   +   +   +   +   +   +   |
E | {}   {}   {}   {}   {}   {}   {}   {}   {} |
  |   +   +   +   +   +   +   +   +   |
F | {}   {}   {}   {}   {}   {}   {}   {}   {} |
  |   +   +   +   +   +   +   +   +   |
G | {}   {}   {}   {}   {}   {}   {}   {}   {} |
  |   +   +   +   +   +   +   +   +   |
H | {}   {}   {}   {}   {}   {}   {}   {}   {} |
  |   +   +   +   +   +   +   +   +   |
I | {}   {}   {}   {}   {}   {}   {}   {}   {} |
  +-----------------------------------+
"""

# def board(state):
#     b  = ''
#     b += 4*' '



class GAME:

    def __init__(self):
        self.size = (9, 9)
        self.state = (self.size[0] * self.size[1])*[' ']
        self.move = None
        
    def __repr__(self):
        return BOARD.format(*self.state)

    def __getstate__(self):
        return self.__dict__
    
    def __setstate__(self, objdict):
        self.__dict__ = objdict

    def bonk(self, target):
        while True:
            try:
                self.move = target.lower()
                connection.send(pickle.dumps(self))
                newstate = pickle.loads(connection.recv(1024)).state.copy()
                if self.state.count('-') < newstate.count('-'):
                    hit = 0
                elif self.state.count('X') < newstate.count('X'):
                    hit = 1
                else:
                    raise ValueError('wtf')
                self.state = newstate
                return hit
            except:
                print('Wut?')

    def hom(self):
        board = pickle.loads(connection.recv(1024))
        target = board.move.lower()
        target = "abcdefghi".index(target[0]) * 9 + "123456789".index(target[1])
        if self.state[target] == 'O':
            board.state[target] = 'X'
            self.state[target] = 'X'
            hit = 1
        else:
            board.state[target] = '-'
            self.state[target] = '-'
            hit = 0
        connection.send(pickle.dumps(board))
        return hit, target

    def place(self):
        ships = {
            'O': 1,
            'OO': 2,
            'OOO': 3,
            'OOOO': 4,
            'OOOOO': 5
        }
        dirs = {
            'left': -1,
            'right': 1,
            'up': -9,
            'down': 9
        }
        for ship in ships:
            while True:
                try:
                    print('Placing "{}":'.format(ship))
                    print(self)
                    pos, dir = input(' > (XX dir) ').lower().split(' ')
                    pos = "abcdefghi".index(pos[0]) * 9 + "123456789".index(pos[1])
                    for i in range(ships[ship]):
                        k = pos + i * dirs[dir]
                        assert self.state[k] == ' '
                        self.state[k] = 'O'
                    break
                except:
                    continue


playerBoard   = GAME()
opponentBoard = GAME()

def show():
    str1 = str(playerBoard).split('\n')
    str2 = str(opponentBoard).split('\n')
    for i in range(len(str1)):
        print(str1[i] + ' '*8 + str2[i])

playerBoard.place()

connection.send(b'\x00')
print('Waiting for other player to finish set-up...')
connection.recv(1024)

if HOST:

    while True:

        show()
        target = input('bonk? > (XX) ')
        hit = opponentBoard.bonk(target)

        if hit:
            print('You hit one of their ships. Get ready to bonk again ~ !')
        else:
            print('You missed QnQ')
            break

while True:

    while True:

        show()
        print('Waiting for other player to bonk...')
        hit, target = playerBoard.hom()

        if hit:
            print('They hit one of your ships at {}... o7'.format(target.upper()))
        else:
            print('The fools missed us at {}~ !'.format(target.upper()))
            break

    while True:

        show()
        target = input('bonk? > (XX) ')
        hit = opponentBoard.bonk(target)

        if hit:
            print('You hit one of their ships. Get ready to bonk again ~ !')
        else:
            print('You missed QnQ')
            break



# game = GAME()

# if HOST:
# 	PLAYER = 'X'
# else:
# 	PLAYER = 'O'

# print('You are "{}":'.format(PLAYER))
# print(BOARD.format(*game.state))

# if HOST:

# 	move = input('Move? (1-9) ')
# 	game.state[int(move) - 1] = PLAYER
    
# 	connection.send(pickle.dumps(game))
# 	print(BOARD.format(*game.state))

# else:

# 	print('Waiting for host to make move...')

# while True:

# 	game = pickle.loads(connection.recv(1024))
# 	print(BOARD.format(*game.state))

# 	move = input('Move? (1-9) ')
# 	game.state[int(move) - 1] = PLAYER
# 	connection.send(pickle.dumps(game))

# 	print(BOARD.format(*game.state))




