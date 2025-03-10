class Board:
    def __init__(self, size=10):
        self.size = size
        self.grid = [['🌊' for _ in range(size)] for _ in range(size)]
        self.ships = []

    def place_ship(self, ship, row, col, is_vertical):
        if is_vertical:
            if row + ship.size > self.size:
                print("Ship placement is out of bounds!")
                return False
            for i in range(ship.size):
                if self.grid[row + i][col] != '🌊':
                    print(f"Position ({row + i}, {col}) is already occupied!")
                    return False
        else:
            if col + ship.size > self.size:
                print("Ship placement is out of bounds!")
                return False
            for i in range(ship.size):
                if self.grid[row][col + i] != '🌊':
                    print(f"Position ({row}, {col + i}) is already occupied!")
                    return False

        for i in range(ship.size):
            if is_vertical:
                self.grid[row + i][col] = '🚢'
                ship.add_positions(row + i, col)
            else:
                self.grid[row][col + i] = '🚢'
                ship.add_positions(row, col + i)

        self.ships.append(ship)
        return True

    def print_board(self, show_ships=False):
        for row in self.grid:
            print(' '.join(block if (block != '🚢' or show_ships) else '🌊' for block in row))