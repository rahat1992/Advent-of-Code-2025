def parse_manifold(input_file):
    """
    Parse the manifold diagram.
    Returns the grid and the starting position.
    """
    with open(input_file, 'r') as f:
        grid = [line.rstrip('\n') for line in f]

    # Find the starting position 'S'
    start_row = -1
    start_col = -1
    for row_idx, row in enumerate(grid):
        for col_idx, char in enumerate(row):
            if char == 'S':
                start_row = row_idx
                start_col = col_idx
                break
        if start_row != -1:
            break

    return grid, start_row, start_col


def simulate_beams(grid, start_row, start_col):
    """
    Simulate the tachyon beams through the manifold.
    Returns the total number of splits.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Queue of active beams: (row, col)
    # Each beam starts at a position and moves downward
    active_beams = [(start_row, start_col)]

    # Track positions where we've already processed splits
    # to avoid counting the same split multiple times
    split_positions = set()

    total_splits = 0

    # Process beams level by level (row by row)
    while active_beams:
        # Move all beams down one row
        new_beams = []

        for row, col in active_beams:
            # Move beam down
            next_row = row + 1

            # Check if beam exits the manifold
            if next_row >= rows:
                continue

            # Check what the beam encounters
            if grid[next_row][col] == '^':
                # Beam hits a splitter
                # Only count this split if we haven't already split here
                if (next_row, col) not in split_positions:
                    split_positions.add((next_row, col))
                    total_splits += 1

                    # Create two new beams: left and right
                    left_col = col - 1
                    right_col = col + 1

                    if left_col >= 0:
                        new_beams.append((next_row, left_col))
                    if right_col < cols:
                        new_beams.append((next_row, right_col))
            else:
                # Beam continues downward (empty space)
                new_beams.append((next_row, col))

        active_beams = new_beams

    return total_splits


def solve_part1(input_file):
    """
    Solve Part 1: Count how many times the beam is split.
    """
    grid, start_row, start_col = parse_manifold(input_file)
    splits = simulate_beams(grid, start_row, start_col)
    return splits


def solve_part2(input_file):
    """
    Solve Part 2: Placeholder for when Part 2 is revealed.
    """
    # Part 2 not yet available
    return None


if __name__ == "__main__":
    print("Part 1:")
    result1 = solve_part1("input.txt")
    print(f"Total beam splits: {result1}")

    print("\nPart 2:")
    result2 = solve_part2("input.txt")
    if result2 is not None:
        print(f"Part 2 result: {result2}")
    else:
        print("Part 2 not yet available")
