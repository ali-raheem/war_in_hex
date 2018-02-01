#!/usr/bin/python
# GPLv3 Ali Raheem 2017
import socket
import select
import argparse
import operator
import pygame
from pygame.locals import *
from sys import exit

from tile import Tile
from game import Game

from json import dumps

def clean_quit():
	if NETWORK:
		conn.close()		
	pygame.quit()
	exit()
def loadTile(path):
	tile = pygame.image.load(path)
	tile.convert_alpha()
	return tile

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--network", action='store', dest='host_port', help="host:port Enable network support.")
parser.add_argument("-s", "--server", action='store_true', dest='server', help="Act as server.")
args = parser.parse_args()

NETWORK = args.host_port
SERVER = args.server

if NETWORK:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	PORT = int(args.host_port.split(':')[1])
	HOST = args.host_port.split(':')[0]
	if SERVER:
		try:
			print ("Waiting for a connection on port %d"%PORT)
			s.bind((HOST, PORT))
			s.listen(1)
			conn, addr = s.accept()
			print "Connection from",addr,"established."
		except:
			print ("Failed to create server, maybe is in use or privelidged.")
			clean_quit()
	else:
		conn = s
		try:
			conn.connect((HOST, PORT))
			print "Connected."
                        try:
                                conn.send(GAME_NAME)
                        except:
                                conn.send("Any")
		except:
			print("Failed to connect to host.")
			clean_quit()
	conn.setblocking(0)
pygame.init()

windowSurface = pygame.display.set_mode((980, 640), 0, 32)
pygame.display.set_caption('War in Hex')

moveSound = pygame.mixer.Sound('assets/tile_drop.wav')

#playAreaSurface = pygame.image.load('assets/playarea.png')
#basicFont = pygame.font.SysFont(None, 48)


sideBoardSurface = pygame.image.load('assets/sideboard.png')

blackGenTile = loadTile('assets/black_general_tile.png')
blackHeliTile = loadTile('assets/black_helicopter_tile.png')
blackBoatTile = loadTile('assets/black_boat_tile.png')
blackInfTile = loadTile('assets/black_troops_tile.png')
blackTankTile = loadTile('assets/black_tank_tile.png')

whiteGenTile = loadTile('assets/white_general_tile.png')
whiteBoatTile = loadTile('assets/white_boat_tile.png')
whiteInfTile = loadTile('assets/white_troops_tile.png')
whiteTankTile = loadTile('assets/white_tank_tile.png')
whiteHeliTile = loadTile('assets/white_helicopter_tile.png')

game = Game(windowSurface)

game.addTile(800, 10, "Black Helicopter 1", blackHeliTile)
game.addTile(850, 10, "Black Helicopter 2", blackHeliTile)
game.addTile(900, 10, "Black Helicopter 3", blackHeliTile)

game.addTile(800, 60, "Black Battleship 1", blackBoatTile)
game.addTile(850, 60, "Black Battleship 2", blackBoatTile)
game.addTile(900, 60, "Black Battleship 3", blackBoatTile)

game.addTile(800, 110, "Black General", blackGenTile)
game.addTile(850, 110, "Black Infantry 1", blackInfTile)
game.addTile(900, 110, "Black Infantry 2", blackInfTile)

game.addTile(800, 160, "Black Tank 1", blackTankTile)
game.addTile(850, 160, "Black Tank 2", blackTankTile)

game.addTile(800, 210, "White Battleship 1", whiteBoatTile)
game.addTile(850, 210, "White Battleship 2", whiteBoatTile)
game.addTile(900, 210, "White Battleship 3", whiteBoatTile)

game.addTile(800, 260, "White General", whiteGenTile)
game.addTile(850, 260, "White Tank 1", whiteTankTile)
game.addTile(900, 260, "White Tank 2", whiteTankTile)

game.addTile(800, 310, "White Infantry 1", whiteInfTile)
game.addTile(850, 310, "White Infantry 2", whiteInfTile)
game.addTile(900, 310, "White Helicopter 1", whiteHeliTile)

game.addTile(800, 360, "White Helicopter 2", whiteHeliTile)
game.addTile(850, 360, "White Helicopter 3", whiteHeliTile)

#windowSurface.blit(playAreaSurface, (0,0))
windowSurface.fill((44, 84, 96))
windowSurface.blit(sideBoardSurface, (750, 0))

game.draw()

pygame.display.update()

#print "Debug:"
#bh2 = game.findTileByName("Black Helicopter 2")
#if(bh2 != None):
#	print (bh2.x, bh2.y)

#print "Debug:"
#wh2 = game.findTileByLocation((850, 360))
#for t in wh2:	
#	print t.name

#print "Debug move"
#game.moveTileByCmd("Black Helicopter 1 from (800, 10) to (324, 275)")
#game.moveTileByCmd("Black General from (800, 110) to (360, 325)")
#game.moveTileByCmd("White General from (800, 260) to (360, 225)")


picked = None
tileStart = (0, 0)
running = True
RENDER_TIMER = pygame.USEREVENT
pygame.time.set_timer(RENDER_TIMER, int(1000/20))
while running:
	pygame.time.wait(10)
	for event in pygame.event.get():
		if event.type == QUIT:
			running = False
		if picked:
			coord = pygame.mouse.get_pos()
			picked.setCenter(coord)
			picked.draw()
		if event.type == MOUSEBUTTONDOWN:
			coord = pygame.mouse.get_pos()
			if picked:
				picked.setCenter(coord)
				game.toTop(picked)
				print picked.name,"from",str(tileStart),"to",str((picked.x, picked.y))
				if NETWORK:
					_, conn_w, _ = select.select([], [conn], [], 0)
					if conn_w != []:
						try:
                                                        move = {}
                                                        move['name'] = picked.name
                                                        move['from'] = tileStart
                                                        move['to'] = (picked.x, picked.y)
							conn_w[0].send(dumps(move))
						except:
							print("Error: Unable to send move over network.")
				moveSound.play()
				picked = None
				continue
			for t in game.tiles:
				if t.isOn(coord):
					picked = t
					tileStart = (t.x, t.y)
#					print "Picked up", t.name
					continue
		if event.type == RENDER_TIMER:
#			windowSurface.blit(playAreaSurface, (0,0))
			windowSurface.fill((44, 84, 96))
			windowSurface.blit(sideBoardSurface, (750, 0))
			game.draw()
			pygame.display.update()
		if NETWORK:
			conn_r, _, _ = select.select([conn], [], [], 0)
			if conn_r != []:
				try:
					a = conn_r[0].recv(1024)
					game.moveTileByCmd(a)
				except:
					print("Error: Unable to recieve move over network.")
clean_quit()
