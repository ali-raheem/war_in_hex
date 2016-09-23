class Game:
	def __init__(self):
		self.tiles = []
	def addTile(self, tile):
		self.tiles.append(tile)
	def draw(self):
		for t in self.tiles:
			t.draw()
	def moveTileByCmd(self, move):
		tileName = move.split(' from')[0]
		tile = self.findTileByName(tileName)
		locationString = move.split(' to ')[1]
		location = locationString.split(',')
		x , y = int(location[0][1:]),int(location[1][:-1])
		tile.setCenter((x,y))
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
