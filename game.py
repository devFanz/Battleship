import os
import random

from player import Player


class Game:
	def __init__(self):
		self.players = []
		self.game_mode = 1
		self.game_modes = {
			1: "Classic Mode",
			2: "Rapid Fire Mode"
		}

	def start_menu(self):
		print(
		"===BATTLESHIP===\n"
        "1. Classic Mode\n"
        "2. Rapid Fire Mode\n"
        "3. Exit"
        )
		demo = Player("Demo", 5)
		demo.auto_place_fleet(True)
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
		
		print("\nSpecial Game Rules:")

		shield_count = 0
		while True:
			try:
				shield_count = int(input(
					"🛡️  Shield 🛡️\n"
					"When hit: Automatically reflects a guaranteed hit to attacker\n"
					"When hit: Reflects guaranteed hit to attacker\n"
					"Shields don't count toward victory\n"
					"🛡️  Number of Shields (0-5) 🛡️\n"
					"Enter number of shields per player (0-5): "
				))
				if 0 <= shield_count <= 5:
					break
				print("Please enter a number between 0-5")
			except ValueError:
				print("Invalid input! Use numbers only")

		p1 = Player("Player 1", shield_count)
		p2 = Player("Player 2", shield_count)
		self.players = [p1, p2]
		
		for player in self.players:
			player.board.print_board(True)
			print(f"\n{player.name}, place your fleet.")
			player.choose_place_fleet_mode()
			print("Pass this to the other player")
			input(f"Press enter for {player.name} turn")
			self.clear_screen()
			
	def show_both_boards(self, attacker, defender):
		print(f"{attacker.name}'s Board'")
		attacker.board.print_board(True)
		print(f"{defender.name}'s Board'")
		defender.board.print_board()

	def play_turn(self, attacker, defender):
		print(f"\n{attacker.name}'s turn:'")
		self.show_both_boards(attacker, defender)
		
		while True:
			try:
				col = int(input("Attack column (1-10): ")) - 1
				row = int(input("Attack row (1-10): ")) - 1

				if not (0 <= row < 10) or not (0 <= col < 10):
					print("Invalid coordinates! Use 1-10")
					continue

				if defender.board.grid[row][col] in ('💥', '💦', '⛨ '):
					print("You already attacked here! Try again.")
					continue

				break
			except ValueError:
				print("Invalid coordinates! Use 1-10")
		
		hit_col = col + 1
		hit_row = row + 1
		hit = False
		shield_ship = None
		if defender.board.grid[row][col] == '🚢':
			print("💥 HIT!💥")
			defender.board.grid[row][col] = '💥'
			for ship in defender.board.ships:
				if (hit_col, hit_row) in ship.positions:
					ship.hits += 1
					if ship.is_sunk():
						print(f"{ship.name} SUNK! 🎯")
			hit = True
		elif defender.board.grid[row][col] == '🛡️ ':
			print("\n💥 SHIELD IMPACT! 💥")
			defender.board.grid[row][col] = '⛨ '
			
			shield_ship = next(
				ship for ship in defender.board.ships 
				if "Shield" in ship.name and (hit_col, hit_row) in ship.positions
			)
			shield_ship.hits = 1
			
			print("🛡️ ENERGY DEFLECTION ACTIVATED!")
			self.deflect_attack(attacker, defender)
		else:
			print("💦 MISS!💦")
			defender.board.grid[row][col] = '💦'
		if not shield_ship:
			defender.board.print_board()
		input("Press enter to continue")
		return hit
		

	def all_sunk(self, player):
		return all(
			ship.is_sunk() 
			for ship in player.board.ships 
			if "Shield" not in ship.name 
		)
	
	def play(self):
		self.clear_screen()
		print(f"===Selected {self.game_modes[self.game_mode]}===\n\n")
		self.setup_board()
		current_player, opponent = self.players
		
		while True:
			self.clear_screen()
			print(f"Pass this to {current_player.name}")
			input("Press enter to continue")
			hit = self.play_turn(current_player, opponent)
			while self.game_mode == 2 and hit:
				hit = self.play_turn(current_player, opponent)
				if self.all_sunk(opponent) or self.all_sunk(current_player):
					break
			if self.all_sunk(opponent):
				print(f"\n🎉 {current_player.name} WINS! 🎉")
				break
			elif self.all_sunk(current_player):
				print(f"\n🎉 {opponent.name} WINS! 🎉")
				break
			current_player, opponent = opponent, current_player
   
	def deflect_attack(self, attacker, defender):
		"""Deflect attack to random valid enemy ship position"""
		viable_targets = []
		for ship in attacker.board.ships:
			if not ship.is_sunk():
				for pos in ship.positions:
					col, row = pos
					if attacker.board.grid[row-1][col-1] == '🚢':
						viable_targets.append((col, row, ship))

		if not viable_targets:
			print("No valid targets for deflection!")
			return

		target_col, target_row, target_ship = random.choice(viable_targets)
		grid_col = target_col - 1
		grid_row = target_row - 1

		attacker.board.grid[grid_row][grid_col] = '💥'
		target_ship.hits += 1
		print(f"🛡️ DEFLECTION HIT! {target_ship.name} at ({target_col}, {target_row})!")

		if target_ship.is_sunk():
			print(f"DEFLECTION SUNK {target_ship.name}! 🎯")

		self.show_both_boards(attacker, defender)

	def clear_screen(self):
		os.system('cls||clear')

if __name__ == "__main__":
	game = Game()
	game.start_menu()