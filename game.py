from player import Player


class Game:
	def __init__(self):
		self.players = []
		
	def setup(self):
		print("===BATTLESHIP===")
		p1 = Player("Player 1")
		p2 = Player("Player 2")
		self.players = [p1, p2]
		
		for player in self.players:
			print(f"\n{player.name}, place your fleet.")
			player.place_fleet()
			
	def play_turn(self, attacker, defender):
		print(f"\n{attacker.name}'s turn:'")
		print(f"{attacker.name}'s Board'")
		attacker.board.print_board(True)
		print(f"{defender.name}'s Board'")
		defender.board.print_board()
		
		while True:
			try:
				row = int(input("Attack row (0-9): "))
				col = int(input("Attack column (0-9): "))

				if not (0 <= row < 10) or not (0 <= col < 10):
					print("Invalid coordinates! Use 0-9")
					continue

				if defender.board.grid[row][col] in ('💥', '💦'):
					print("You already attacked here! Try again.")
					continue

				break
			except ValueError:
				print("Invalid coordinates! Use 0-9")
		
		if defender.board.grid[row][col] == '🚢':
			print("💥 HIT!💥")
			defender.board.grid[row][col] = '💥'
			# Update ship hits
			for ship in defender.board.ships:
				if (row, col) in ship.positions:
					ship.hits += 1
					if ship.is_sunk():
						print(f"{ship.name} SUNK! 🎯")
		else:
			print("💦 MISS!💦")
			defender.board.grid[row][col] = '💦'
		defender.board.print_board()
		input()
		

	def all_sunk(self, player):
		return all(ship.is_sunk() for ship in player.board.ships)
	
	def play(self):
		self.setup()
		current_player, opponent = self.players
		
		while True:
			self.play_turn(current_player, opponent)
			if self.all_sunk(opponent):
				print(f"\n🎉 {current_player.name} WINS! 🎉")
				break
			current_player, opponent = opponent, current_player

if __name__ == "__main__":
	game = Game()
	game.play()