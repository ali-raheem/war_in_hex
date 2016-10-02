#!/usr/bin/python
import operator
import pygame
from pygame.locals import *
from sys import exit

from tile import Tile
from game import Game

def loadTile(path):
	tile = pygame.image.load(path)
	tile.convert_alpha()
	return tile

pygame.init()

windowSurface = pygame.display.set_mode((980, 640), 0, 32)
pygame.display.set_caption('War in Hex')

moveSound = pygame.mixer.Sound('assets/tile_drop.wav')

playAreaSurface = pygame.image.load('assets/playarea.png')
basicFont = pygame.font.SysFont(None, 48)


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

windowSurface.blit(playAreaSurface, (0,0))
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
			windowSurface.blit(playAreaSurface, (0,0))
			windowSurface.blit(sideBoardSurface, (750, 0))
			game.draw()
			pygame.display.update()

		
pygame.quit()
exit()
