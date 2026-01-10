def solve_part1(input_file):
    """
    Solve Part 1: Count how many times the dial ends at 0 after a rotation.
    """
    # Read the input file
    with open(input_file, 'r') as f:
        rotations = [line.strip() for line in f if line.strip()]

    # Start position
    position = 50
    count_zeros = 0

    # Process each rotation
    for rotation in rotations:
        direction = rotation[0]  # 'L' or 'R'
        distance = int(rotation[1:])  # The number after L or R

        # Apply the rotation
        if direction == 'L':
            position = (position - distance) % 100
        else:  # direction == 'R'
            position = (position + distance) % 100

        # Check if we landed on 0
        if position == 0:
            count_zeros += 1

    return count_zeros


def solve_part2(input_file):
    """
    Solve Part 2: Count how many times the dial points at 0 during or after any rotation.
    This includes all clicks that pass through 0, not just ending positions.
    """
    # Read the input file
    with open(input_file, 'r') as f:
        rotations = [line.strip() for line in f if line.strip()]

    # Start position
    position = 50
    count_zeros = 0

    # Process each rotation
    for rotation in rotations:
        direction = rotation[0]  # 'L' or 'R'
        distance = int(rotation[1:])  # The number after L or R

        # Count how many times we pass through 0 during this rotation
        # We need to count complete cycles through 0

        if direction == 'L':
            # Moving left (decreasing)
            # Calculate how many times we cross 0
            # We cross 0 when we go from 1,2,... to 99,98,...
            new_position = (position - distance) % 100

            # How many complete cycles?
            full_cycles = distance // 100
            count_zeros += full_cycles

            # Check if we cross 0 in the partial cycle
            remaining = distance % 100
            if remaining > position:
                # We crossed 0
                count_zeros += 1

        else:  # direction == 'R'
            # Moving right (increasing)
            # Calculate how many times we cross 0
            # We cross 0 when we go from 99 to 0
            new_position = (position + distance) % 100

            # How many complete cycles?
            full_cycles = distance // 100
            count_zeros += full_cycles

            # Check if we cross 0 in the partial cycle
            remaining = distance % 100
            if position + remaining >= 100:
                # We crossed 0
                count_zeros += 1

        position = new_position

    return count_zeros


if __name__ == "__main__":
    print("Part 1:")
    result1 = solve_part1("input.txt")
    print(f"The password is: {result1}")

    print("\nPart 2:")
    result2 = solve_part2("input.txt")
    print(f"The password is: {result2}")
