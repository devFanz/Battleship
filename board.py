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

    def place_ship(self, ship, start_col, start_row, is_vertical):
        # Convert to 0-based indices
        col = start_col - 1
        row = start_row - 1

        # Validate input
        if not (0 <= col < self.size) or not (0 <= row < self.size):
            print(f"Coordinates must be between 1 and {self.size}!")
            return False

        # Check vertical placement
        if is_vertical:
            if row + ship.size > self.size:
                print(f"Needs {ship.size} rows starting from row {start_row}!")
                return False
            for i in range(ship.size):
                if self.grid[row+i][col] != '🌊':
                    print(f"Column {start_col}, row {start_row+i} is occupied!")
                    return False
        # Check horizontal placement
        else:  
            if col + ship.size > self.size:
                print(f"Needs {ship.size} columns starting from column {start_col}!")
                return False
            for i in range(ship.size):
                if self.grid[row][col+i] != '🌊':
                    print(f"Column {start_col+i}, row {start_row} is occupied!")
                    return False

        # Place the ship
        for i in range(ship.size):
            if is_vertical:
                self.grid[row+i][col] = '🚢'
                ship.add_positions(start_row+i, start_col)  # Store as (row, col)
            else:
                self.grid[row][col+i] = '🚢'
                ship.add_positions(start_row, start_col+i)

        self.ships.append(ship)
        return True