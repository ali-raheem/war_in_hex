#!/usr/bin/python
import operator
import pygame
from pygame.locals import *
from sys import exit

from tile import Tile

pygame.init()


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
tiles.append(Tile(800, 10, "Black Helicopter 1", blackHeliTile))
tiles.append(Tile(850, 10, "Black Helicopter 2", blackHeliTile))
tiles.append(Tile(900, 10, "Black Helicopter 3", blackHeliTile))

tiles.append(Tile(800, 60, "Black Battleship 1", blackBoatTile))
tiles.append(Tile(850, 60, "Black Battleship 2", blackBoatTile))
tiles.append(Tile(900, 60, "Black Battleship 3", blackBoatTile))

tiles.append(Tile(800, 110, "Black General", blackGenTile))
tiles.append(Tile(850, 110, "Black Troops 1", blackTroopsTile))
tiles.append(Tile(900, 110, "Black Troops 2", blackTroopsTile))

tiles.append(Tile(800, 160, "Black Tank 1", blackTankTile))
tiles.append(Tile(850, 160, "Black Tank 2", blackTankTile))

tiles.append(Tile(800, 210, "White Battleship 1", whiteBoatTile))
tiles.append(Tile(850, 210, "White Battleship 2", whiteBoatTile))
tiles.append(Tile(900, 210, "White Battleship 3", whiteBoatTile))

tiles.append(Tile(800, 260, "White General", whiteGenTile))
tiles.append(Tile(850, 260, "White Tank 1", whiteTankTile))
tiles.append(Tile(900, 260, "White Tank 2", whiteTankTile))

tiles.append(Tile(800, 310, "White Bettle 1", whiteTroopsTile))
tiles.append(Tile(850, 310, "White Bettle 2", whiteTroopsTile))
tiles.append(Tile(900, 310, "White Helicopter 1", whiteHeliTile))

tiles.append(Tile(800, 360, "White Helicopter 2", whiteHeliTile))
tiles.append(Tile(850, 360, "White Helicopter 3", whiteHeliTile))

for t in tiles:
	t.draw(windowSurface)

pygame.display.update()

picked = None
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit()
		if picked:
			coord = pygame.mouse.get_pos()
			picked.setCenter(coord)
			picked.draw(windowSurface)
		if event.type == MOUSEBUTTONDOWN:
			coord = pygame.mouse.get_pos()
			if picked:
				picked.setCenter(coord)
				print "Putdown up", picked.name
				tiles.remove(picked)
				tiles.append(picked)
				picked = None
				continue
			for t in tiles:
				if t.isOn(coord):
					picked = t
					print "Picked up", t.name
					continue

	windowSurface.blit(playAreaSurface, (0,0))
	windowSurface.blit(sideBoardSurface, (750, 0))

	for t in tiles:
		t.draw(windowSurface)

	pygame.display.update()


		
