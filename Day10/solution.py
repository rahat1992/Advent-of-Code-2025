def parse_input(input_file):
    """
    Parse the input file.
    Returns the parsed data structure.
    """
    with open(input_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines


def solve_part1(input_file):
    """
    Solve Part 1.
    """
    data = parse_input(input_file)
    # TODO: Implement solution
    return 0


def solve_part2(input_file):
    """
    Solve Part 2.
    """
    data = parse_input(input_file)
    # TODO: Implement solution
    return 0


if __name__ == "__main__":
    print("Part 1:")
    result1 = solve_part1("input.txt")
    print(f"Result: {result1}")

    print("\nPart 2:")
    result2 = solve_part2("input.txt")
    print(f"Result: {result2}")
