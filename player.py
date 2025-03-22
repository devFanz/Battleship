import random

from board import Board
from ship import Ship


class Player:
	def __init__(self, name, shield_count=0):
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
		for i in range(1, shield_count+1):
			self.ships.append((f"Shield {i}", 1))
	def place_fleet(self):
		for ship_name, ship_size in self.ships:
			placed = False
			while not placed:
				print(f"Place your {ship_name} (Size: {ship_size})")
				
				try:
					col = int(input("Enter column (1-10): "))
					row = int(input("Enter row (1-10): "))
					vertical = input("Vertical? (y/n): ").lower() == 'y' if ship_size > 1 else "0"
				except ValueError:
					print("Invalid input! Use numbers 1-10")
					continue
				
				placed = self.board.place_ship(Ship(ship_name, ship_size), col, row, vertical)
				
				if not placed:
					print("Invalid position! The ship is out of range. Try again")
				else:
					self.board.print_board(True)

	def auto_place_fleet(self, demo=False):
		for ship_name, ship_size in self.ships:
			placed = False
			while not placed:
				col = random.randint(1, self.board.size)
				row = random.randint(1, self.board.size)
				vertical = random.choice([True, False])
				
				ship = Ship(ship_name, ship_size)
				
				placed = self.board.place_ship(ship, col, row, vertical, True)
		if not demo:
			print(f"{self.name}'s ships have been placed automatically!")
		self.board.print_board(True)

	def choose_place_fleet_mode(self):
		chosen = False
		print("Choose your placing mode\n"
		"1. Manual\n"
		"2. Randomly selected")

		while True:
			mode = input("Select mode:")
			try:
				mode = int(mode)
			except ValueError:
				print(f"Invalid number: '{mode}'. Please enter a valid numeric string.")
				continue
			self.game_mode = mode
			if self.game_mode == 1:
				self.place_fleet()
				break
			elif self.game_mode == 2:
				self.auto_place_fleet()
				break
			else:
				print("Invalid choice! Please enter 1 or 2")