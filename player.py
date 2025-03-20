from board import Board
from ship import Ship


class Player:
	def __init__(self, name):
		self.name = name
		self.board = Board()
		# self.enemy_board = Board()
		self.ships = [
		("Carrier", 5),
		("Battleship", 4),
		("Cruiser", 3),
		("Submarine", 3),
		("Destroyer", 2)
		]
		# self.ships = [
		# ("Carrier", 5)
		# ]
	def place_fleet(self):
		for ship_name, ship_size in self.ships:
			placed = False
			while not placed:
				print(f"Place your {ship_name} (Size: {ship_size})")
				# print(f"The ship will be placed at the row ")
				
				try:
					row = int(input("Enter row (1-10): "))
					col = int(input("Enter column (1-10): "))
					vertical = input("Vertical? (y/n): ").lower() == 'y'
				except ValueError:
					print("invalid input! Use numbers 1-10")
					continue
				
				placed = self.board.place_ship(Ship(ship_name,ship_size),row, col, vertical)

				if not placed:
					print("Invalid position! The ship is out of range, Try again")
				else:
					self.board.print_board(True)
