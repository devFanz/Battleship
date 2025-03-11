class Ship:
	def __init__(self, name, size):
		self.name = name
		self.size = size
		self.hits = 0
		self.positions = []
		self.is_vertical = False
		
	def is_sunk(self):
		return self.hits >= self.size
	
	def add_positions(self, row, col):
		self.positions.append((row, col))
	