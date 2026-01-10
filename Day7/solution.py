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


def simulate_quantum_particle(grid, start_row, start_col):
    """
    Simulate a quantum tachyon particle that takes both paths at each splitter.
    Returns the number of unique timelines.

    Use dynamic programming: track the number of distinct paths to each position.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Track number of paths to each position: {(row, col): num_paths}
    current_positions = {(start_row, start_col): 1}
    total_exited = 0

    # Process row by row
    for current_row in range(start_row, rows):
        next_positions = {}

        for (row, col), num_paths in current_positions.items():
            if row != current_row:
                continue

            # Move particle down
            next_row = row + 1

            # Check if particle exits the manifold
            if next_row >= rows:
                # These paths complete - count them
                total_exited += num_paths
                continue

            # Check what the particle encounters
            if grid[next_row][col] == '^':
                # Particle hits a splitter - it takes BOTH paths
                left_col = col - 1
                right_col = col + 1

                if left_col >= 0:
                    if (next_row, left_col) not in next_positions:
                        next_positions[(next_row, left_col)] = 0
                    next_positions[(next_row, left_col)] += num_paths

                if right_col < cols:
                    if (next_row, right_col) not in next_positions:
                        next_positions[(next_row, right_col)] = 0
                    next_positions[(next_row, right_col)] += num_paths
            else:
                # Particle continues downward
                if (next_row, col) not in next_positions:
                    next_positions[(next_row, col)] = 0
                next_positions[(next_row, col)] += num_paths

        # Update current_positions for next iteration
        current_positions = {pos: count for pos, count in current_positions.items() if pos[0] != current_row}
        current_positions.update(next_positions)

    return total_exited


def solve_part2(input_file):
    """
    Solve Part 2: Count the number of different timelines.
    """
    grid, start_row, start_col = parse_manifold(input_file)
    timelines = simulate_quantum_particle(grid, start_row, start_col)
    return timelines


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
