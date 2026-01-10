def count_adjacent_rolls(grid, row, col):
    """
    Count the number of rolls (@) adjacent to the position (row, col).
    Adjacent means the 8 surrounding positions (including diagonals).
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    count = 0
    # Check all 8 directions: up, down, left, right, and 4 diagonals
    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # top-left, top, top-right
        (0, -1),           (0, 1),    # left, right
        (1, -1),  (1, 0),  (1, 1)     # bottom-left, bottom, bottom-right
    ]

    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc

        # Check if the position is within bounds
        if 0 <= new_row < rows and 0 <= new_col < cols:
            if grid[new_row][new_col] == '@':
                count += 1

    return count


def count_accessible_rolls(grid):
    """
    Count the number of rolls that are accessible by a forklift.
    A roll is accessible if it has fewer than 4 adjacent rolls.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    accessible_count = 0

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == '@':
                adjacent_count = count_adjacent_rolls(grid, row, col)
                if adjacent_count < 4:
                    accessible_count += 1

    return accessible_count


def remove_accessible_rolls(grid):
    """
    Remove all accessible rolls from the grid and return the count removed.
    A roll is accessible if it has fewer than 4 adjacent rolls.
    Returns a tuple: (modified grid, count of rolls removed)
    """
    # Convert grid to list of lists for mutability
    grid_list = [list(row) for row in grid]
    rows = len(grid_list)
    cols = len(grid_list[0]) if rows > 0 else 0

    # Find all accessible rolls
    to_remove = []
    for row in range(rows):
        for col in range(cols):
            if grid_list[row][col] == '@':
                adjacent_count = count_adjacent_rolls(grid_list, row, col)
                if adjacent_count < 4:
                    to_remove.append((row, col))

    # Remove them
    for row, col in to_remove:
        grid_list[row][col] = '.'

    # Convert back to list of strings
    new_grid = [''.join(row) for row in grid_list]

    return new_grid, len(to_remove)


def count_total_removable_rolls(grid):
    """
    Count the total number of rolls that can be removed by repeatedly
    removing accessible rolls until no more can be removed.
    """
    total_removed = 0
    current_grid = grid[:]

    while True:
        current_grid, removed = remove_accessible_rolls(current_grid)
        if removed == 0:
            break
        total_removed += removed

    return total_removed


def solve_part1(input_file):
    """
    Solve Part 1: Count how many rolls of paper can be accessed by a forklift.
    """
    with open(input_file, 'r') as f:
        grid = [line.strip() for line in f if line.strip()]

    accessible_rolls = count_accessible_rolls(grid)

    return accessible_rolls


def solve_part2(input_file):
    """
    Solve Part 2: Count how many rolls can be removed in total by repeatedly
    removing accessible rolls.
    """
    with open(input_file, 'r') as f:
        grid = [line.strip() for line in f if line.strip()]

    total_removable = count_total_removable_rolls(grid)

    return total_removable


if __name__ == "__main__":
    print("Part 1:")
    result1 = solve_part1("input.txt")
    print(f"Number of accessible rolls: {result1}")

    print("\nPart 2:")
    result2 = solve_part2("input.txt")
    print(f"Total rolls that can be removed: {result2}")
