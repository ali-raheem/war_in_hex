class Tile:
	def __init__(self, x, y, name, image, surface):
		self.x = x
		self.y = y
		self.name = name
		self.image = image
		self.surface = surface
		return
	def setCenter(self, loc):
		x,y = loc
#		print loc
		x -= 25
#		y -= 25
		x = x/12 * 12
		y = y/21 * 21
#		print (x,y)
		self.x, self.y = x, y
		return
	def draw(self):
		self.surface.blit(self.image, (self.x, self.y))
	def isOn(self, cord):
		x, y = cord
		return (x >= self.x) & (x <= self.x+50) & (y >= self.y) & (y <= self.y + 50)
