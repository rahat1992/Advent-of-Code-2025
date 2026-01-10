def parse_worksheet(input_file):
    """
    Parse the math worksheet into individual problems.
    Returns a list of (numbers, operation) tuples.
    """
    with open(input_file, 'r') as f:
        lines = [line.rstrip('\n') for line in f]

    # Remove any trailing empty lines
    while lines and not lines[-1].strip():
        lines.pop()

    if not lines:
        return []

    # The last line contains operations
    operations_line = lines[-1]
    number_lines = lines[:-1]

    # Find the width of the worksheet
    max_width = max(len(line) for line in lines)

    # Pad all lines to the same width
    padded_lines = []
    for line in number_lines:
        padded_lines.append(line.ljust(max_width))
    operations_line = operations_line.ljust(max_width)

    # Identify columns (problems are separated by full columns of spaces)
    problems = []
    col = 0

    while col < max_width:
        # Skip spaces
        while col < max_width and all(line[col] == ' ' for line in padded_lines) and operations_line[col] == ' ':
            col += 1

        if col >= max_width:
            break

        # Found start of a problem - find its width
        start_col = col
        while col < max_width and not (all(line[col] == ' ' for line in padded_lines) and operations_line[col] == ' '):
            col += 1
        end_col = col

        # Extract this problem
        numbers = []
        for line in padded_lines:
            num_str = line[start_col:end_col].strip()
            if num_str:
                numbers.append(int(num_str))

        operation = operations_line[start_col:end_col].strip()

        if numbers and operation:
            problems.append((numbers, operation))

    return problems


def solve_problem(numbers, operation):
    """
    Solve a single math problem.
    numbers: list of integers to combine
    operation: either '*' or '+'
    """
    if not numbers:
        return 0

    result = numbers[0]
    for num in numbers[1:]:
        if operation == '*':
            result *= num
        elif operation == '+':
            result += num

    return result


def solve_part1(input_file):
    """
    Solve Part 1: Calculate the grand total of all problems on the worksheet.
    """
    problems = parse_worksheet(input_file)

    grand_total = 0
    for numbers, operation in problems:
        answer = solve_problem(numbers, operation)
        grand_total += answer

    return grand_total


def parse_worksheet_rtl(input_file):
    """
    Parse the math worksheet reading right-to-left.
    Each number is read column-by-column with the most significant digit at the top.
    Returns a list of (numbers, operation) tuples.
    """
    with open(input_file, 'r') as f:
        lines = [line.rstrip('\n') for line in f]

    # Remove any trailing empty lines
    while lines and not lines[-1].strip():
        lines.pop()

    if not lines:
        return []

    # The last line contains operations
    operations_line = lines[-1]
    number_lines = lines[:-1]

    # Find the width of the worksheet
    max_width = max(len(line) for line in lines)

    # Pad all lines to the same width
    padded_lines = []
    for line in number_lines:
        padded_lines.append(line.ljust(max_width))
    operations_line = operations_line.ljust(max_width)

    # Identify problem columns (problems are separated by full columns of spaces)
    problems = []
    col = 0

    while col < max_width:
        # Skip spaces
        while col < max_width and all(line[col] == ' ' for line in padded_lines) and operations_line[col] == ' ':
            col += 1

        if col >= max_width:
            break

        # Found start of a problem - find its width
        start_col = col
        while col < max_width and not (all(line[col] == ' ' for line in padded_lines) and operations_line[col] == ' '):
            col += 1
        end_col = col

        # Extract this problem reading RIGHT-TO-LEFT
        # Each column within the problem is a separate number
        numbers = []

        # Process each column from right to left
        for c in range(end_col - 1, start_col - 1, -1):
            # Read vertically down this column to build the number
            digits = []
            for line in padded_lines:
                if c < len(line) and line[c] != ' ':
                    digits.append(line[c])

            if digits:
                # The digits are already in order (top to bottom = most to least significant)
                number = int(''.join(digits))
                numbers.append(number)

        # Get the operation (should be consistent across the problem width)
        operation = operations_line[start_col:end_col].strip()

        if numbers and operation:
            problems.append((numbers, operation))

    return problems


def solve_part2(input_file):
    """
    Solve Part 2: Calculate the grand total reading problems right-to-left.
    """
    problems = parse_worksheet_rtl(input_file)

    grand_total = 0
    for numbers, operation in problems:
        answer = solve_problem(numbers, operation)
        grand_total += answer

    return grand_total


if __name__ == "__main__":
    print("Part 1:")
    result1 = solve_part1("input.txt")
    print(f"Grand total: {result1}")

    print("\nPart 2:")
    result2 = solve_part2("input.txt")
    if result2 is not None:
        print(f"Part 2 result: {result2}")
    else:
        print("Part 2 not yet available")
