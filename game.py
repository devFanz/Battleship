import os
import platform

from player import Player


class Game:
	def __init__(self):
		self.players = []
		self.game_mode = 1

	def start_menu(self):
		# print("===BATTLESHIP===")
		print("""
		===BATTLESHIP===
        1. Classic Mode
        2. Rapid Fire Mode
        3. Exit
        """)
		while True:
			mode = input("Select mode:")
			try:
				mode = int(mode)
			except ValueError:
				print(f"Invalid number: '{mode}'. Please enter a valid numeric string.")
				continue
			self.game_mode = mode
			if self.game_mode == 1 or self.game_mode == 2:
				self.play()
				break
			elif self.game_mode == 3:
				exit()
			else:
				print("Invalid choice! Please enter 1-3")
			
	def setup_board(self):
		p1 = Player("Player 1")
		p2 = Player("Player 2")
		self.players = [p1, p2]
		
		for player in self.players:
			player.board.print_board()
			print(f"\n{player.name}, place your fleet.")
			player.place_fleet()
			print("Pass this to the other player")
			input(f"Press enter for {player.name} turn")
			self.clear_screen()
			# print("\033[H\033[J", end="")
			
	def play_turn(self, attacker, defender):
		print(f"\n{attacker.name}'s turn:'")
		print(f"{attacker.name}'s Board'")
		attacker.board.print_board(True)
		print(f"{defender.name}'s Board'")
		defender.board.print_board()
		
		while True:
			try:
				row = int(input("Attack row (1-10): ")) - 1
				col = int(input("Attack column (1-10): ")) - 1

				if not (0 <= row < 10) or not (0 <= col < 10):
					print("Invalid coordinates! Use 1-10")
					continue

				if defender.board.grid[row][col] in ('💥', '💦'):
					print("You already attacked here! Try again.")
					continue

				break
			except ValueError:
				print("Invalid coordinates! Use 1-10")
		
		hit = False
		if defender.board.grid[row][col] == '🚢':
			print("💥 HIT!💥")
			defender.board.grid[row][col] = '💥'
			# Update ship hits
			for ship in defender.board.ships:
				if (row, col) in ship.positions:
					ship.hits += 1
					if ship.is_sunk():
						print(f"{ship.name} SUNK! 🎯")
			hit = True
		else:
			print("💦 MISS!💦")
			defender.board.grid[row][col] = '💦'
		defender.board.print_board()
		input("Press enter to conitnue")
		return hit
		

	def all_sunk(self, player):
		return all(ship.is_sunk() for ship in player.board.ships)
	
	def play(self):
		self.setup_board()
		current_player, opponent = self.players
		
		while True:
			self.clear_screen()
			# print("\033[H\033[J", end="")
			print(f"Pass this to {current_player.name}")
			input("Press enter to conitnue")
			hit = self.play_turn(current_player, opponent)
			while self.game_mode == 2 and hit:
				hit = self.play_turn(current_player, opponent)
			if self.all_sunk(opponent):
				print(f"\n🎉 {current_player.name} WINS! 🎉")
				break
			current_player, opponent = opponent, current_player

	def clear_screen(self):
		# if platform.system() == 'Windows':
		# 	os.system('cls')
		# else:  # Linux/Mac
		# 	os.system('clear')
		os.system('cls||clear')

if __name__ == "__main__":
	game = Game()
	game.start_menu()