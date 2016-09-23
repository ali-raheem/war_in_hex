#!/usr/bin/python
import operator
import pygame
from pygame.locals import *
from sys import exit

from tile import Tile

pygame.init()

def moveTileByCmd(tiles, move):
	tileName = move.split(' from')[0]
	tile = findTileByName(tiles, tileName)
	locationString = move.split(' to ')[1]
	location = locationString.split(',')
	x , y = int(location[0][1:]),int(location[1][:-1])
	tile.setCenter((x,y))

def findTileByName(tiles, name):
	for t in tiles:
		if(t.name == name):
			return t
	return None

def fineTileByLocation(tiles, location):
	x, y = location
	tileList = []
	for t in tiles:
		if((t.x, t.y) ==  location):
			tileList.append(t)
	return tileList

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

windowSurface = pygame.display.set_mode((980, 640), 0, 32)
pygame.display.set_caption('War in Hex')

playAreaSurface = pygame.image.load('assets/playarea.png')
basicFont = pygame.font.SysFont(None, 48)


sideBoardSurface = pygame.image.load('assets/sideboard.png')

blackGenTile = pygame.image.load('assets/black_general_tile.png')
blackGenTile.convert_alpha()
blackHeliTile = pygame.image.load('assets/black_helicopter_tile.png')
blackHeliTile.convert_alpha()
blackBoatTile = pygame.image.load('assets/black_boat_tile.png')
blackBoatTile.convert_alpha()
blackTroopsTile = pygame.image.load('assets/black_troops_tile.png')
blackTroopsTile.convert_alpha()
blackTankTile = pygame.image.load('assets/black_tank_tile.png')
blackTankTile.convert_alpha()

whiteGenTile = pygame.image.load('assets/white_general_tile.png')
whiteGenTile.convert_alpha()
whiteBoatTile = pygame.image.load('assets/white_boat_tile.png')
whiteBoatTile.convert_alpha()
whiteTroopsTile = pygame.image.load('assets/white_troops_tile.png')
whiteTroopsTile.convert_alpha()
whiteTankTile = pygame.image.load('assets/white_tank_tile.png')
whiteTankTile.convert_alpha()
whiteHeliTile = pygame.image.load('assets/white_helicopter_tile.png')
whiteHeliTile.convert_alpha()

windowSurface.blit(playAreaSurface, (0,0))
windowSurface.blit(sideBoardSurface, (750, 0))

tiles = []
tiles.append(Tile(800, 10, "Black Helicopter 1", blackHeliTile, windowSurface))
tiles.append(Tile(850, 10, "Black Helicopter 2", blackHeliTile, windowSurface))
tiles.append(Tile(900, 10, "Black Helicopter 3", blackHeliTile, windowSurface))

tiles.append(Tile(800, 60, "Black Battleship 1", blackBoatTile, windowSurface))
tiles.append(Tile(850, 60, "Black Battleship 2", blackBoatTile, windowSurface))
tiles.append(Tile(900, 60, "Black Battleship 3", blackBoatTile, windowSurface))

tiles.append(Tile(800, 110, "Black General", blackGenTile, windowSurface))
tiles.append(Tile(850, 110, "Black Troops 1", blackTroopsTile, windowSurface))
tiles.append(Tile(900, 110, "Black Troops 2", blackTroopsTile, windowSurface))

tiles.append(Tile(800, 160, "Black Tank 1", blackTankTile, windowSurface))
tiles.append(Tile(850, 160, "Black Tank 2", blackTankTile, windowSurface))

tiles.append(Tile(800, 210, "White Battleship 1", whiteBoatTile, windowSurface))
tiles.append(Tile(850, 210, "White Battleship 2", whiteBoatTile, windowSurface))
tiles.append(Tile(900, 210, "White Battleship 3", whiteBoatTile, windowSurface))

tiles.append(Tile(800, 260, "White General", whiteGenTile, windowSurface))
tiles.append(Tile(850, 260, "White Tank 1", whiteTankTile, windowSurface))
tiles.append(Tile(900, 260, "White Tank 2", whiteTankTile, windowSurface))

tiles.append(Tile(800, 310, "White Bettle 1", whiteTroopsTile, windowSurface))
tiles.append(Tile(850, 310, "White Bettle 2", whiteTroopsTile, windowSurface))
tiles.append(Tile(900, 310, "White Helicopter 1", whiteHeliTile, windowSurface))

tiles.append(Tile(800, 360, "White Helicopter 2", whiteHeliTile, windowSurface))
tiles.append(Tile(850, 360, "White Helicopter 3", whiteHeliTile, windowSurface))

for t in tiles:
	t.draw()

pygame.display.update()

print "Debug:"
bh2 = findTileByName(tiles, "Black Helicopter 2")
if(bh2 != None):
	print (bh2.x, bh2.y)

print "Debug:"
wh2 = fineTileByLocation(tiles, (850, 360))
for t in wh2:	
	print t.name

print "Debug move"
moveTileByCmd(tiles, "Black Helicopter 1 from (800, 10) to (324, 275)")
moveTileByCmd(tiles, "Black General from (800, 110) to (360, 325)")
moveTileByCmd(tiles, "White General from (800, 260) to (360, 225)")


picked = None
tileStart = (0, 0)

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit()
		if picked:
			coord = pygame.mouse.get_pos()
			picked.setCenter(coord)
			picked.draw()
		if event.type == MOUSEBUTTONDOWN:
			coord = pygame.mouse.get_pos()
			if picked:
				picked.setCenter(coord)
#				print "Putdown up", picked.name
				tiles.remove(picked)
				tiles.append(picked)
				print picked.name,"from",str(tileStart),"to",str((picked.x, picked.y))
				picked = None
				continue
			for t in tiles:
				if t.isOn(coord):
					picked = t
					tileStart = (t.x, t.y)
#					print "Picked up", t.name
					continue

	windowSurface.blit(playAreaSurface, (0,0))
	windowSurface.blit(sideBoardSurface, (750, 0))

	for t in tiles:
		t.draw()

	pygame.display.update()


		
