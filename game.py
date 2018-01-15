from json import loads
from tile import Tile

class Game:
	def __init__(self, surface):
		self.surface = surface
		self.tiles = []
	def addTile(self, x, y, name, image):
		tile = Tile(x, y, name, image, self.surface)
		self.tiles.append(tile)
	def draw(self):
		for t in self.tiles:
			t.draw()
	def moveTileByCmd(self, move):
		try:
                        move = loads(move);
			tileName = move['name']
			tile = self.findTileByName(tileName)
			x, y = move['to']
			tile.x = x
			tile.y = y
			self.toTop(tile)
		except:
			pass
	def toTop(self, tile):
		self.tiles.remove(tile)
		self.tiles.append(tile)
	def findTileByName(self, name):
		for t in self.tiles:
			if(t.name == name):
				return t
		return None

	def findTileByLocation(self, location):
		x, y = location
		tileList = []
		for t in self.tiles:
			if((t.x, t.y) ==  location):
				tileList.append(t)
		return tileList
