class Board:
    def __init__(self, size=10):
        self.size = size
        self.grid = [['🌊' for _ in range(size)] for _ in range(size)]
        self.ships = []
        self.num_emoji = ['⏹️ ', '1️⃣ ', '2️⃣ ', '3️⃣ ', '4️⃣ ', '5️⃣ ', '6️⃣ ', '7️⃣ ', '8️⃣ ', '9️⃣ ', '🔟']

    def print_board(self, show_ships=False):

        # Top border with numbers
        edge = [self.num_emoji[0]] + self.num_emoji[1:self.size+1] + [self.num_emoji[0]]
        print(' '.join(c for c in edge))

        # Board rows
        for i, row in enumerate(self.grid):
            side_num = self.num_emoji[i+1]
            cells = [side_num] + [self._format_cell(cell, show_ships) for cell in row] + [side_num]
            print(' '.join(c for c in cells))

        # Bottom border with numbers
        print(' '.join(c for c in edge))

    def _format_cell(self, cell, show_ships):
        if cell == '🚢' and not show_ships:
            return '🌊'
        return cell

    def place_ship(self, ship, row, col, is_vertical):
        
        row -= 1
        col -= 1
        
        # Validate input range
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            print(f"Coordinates must be between 1 and {self.size}!")
            return False

        # Check boundaries
        if is_vertical:
            if row + ship.size > self.size:
                print(f"Ship needs {ship.size} vertical spaces starting at row {row+1}!")
                return False
            for i in range(ship.size):
                if self.grid[row+i][col] != '🌊':
                    print(f"Row {row+i+1}, column {col+1} is occupied!")
                    return False
        else:
            if col + ship.size > self.size:
                print(f"Ship needs {ship.size} horizontal spaces starting at column {col+1}!")
                return False
            for i in range(ship.size):
                if self.grid[row][col+i] != '🌊':
                    print(f"Row {row+1}, column {col+i+1} is occupied!")
                    return False

        # Place the ship
        for i in range(ship.size):
            if is_vertical:
                self.grid[row+i][col] = '🚢'
                ship.add_positions(row+i+1, col+1)  # Store 1-based positions
            else:
                self.grid[row][col+i] = '🚢'
                ship.add_positions(row+1, col+i+1)

        self.ships.append(ship)
        return True