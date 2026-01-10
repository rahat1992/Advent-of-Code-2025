def is_invalid_id_part1(num):
    """
    Check if a number is an invalid ID for Part 1.
    Invalid IDs are numbers where a sequence of digits is repeated exactly twice.
    Examples: 55 (5 twice), 6464 (64 twice), 123123 (123 twice)
    """
    num_str = str(num)
    length = len(num_str)

    # Must be even length to be repeated twice
    if length % 2 != 0:
        return False

    # Split in half and check if both halves are identical
    mid = length // 2
    first_half = num_str[:mid]
    second_half = num_str[mid:]

    # Check if the first half has no leading zeros (to avoid 0101)
    # and if both halves are identical
    if first_half[0] == '0':
        return False

    return first_half == second_half


def is_invalid_id_part2(num):
    """
    Check if a number is an invalid ID for Part 2.
    Invalid IDs are numbers where a sequence of digits is repeated at least twice.
    Examples:
    - 12341234 (1234 two times)
    - 123123123 (123 three times)
    - 1212121212 (12 five times)
    - 1111111 (1 seven times)
    """
    num_str = str(num)
    length = len(num_str)

    # Try all possible pattern lengths from 1 to length//2
    for pattern_len in range(1, length // 2 + 1):
        # Check if the total length is divisible by the pattern length
        if length % pattern_len == 0:
            pattern = num_str[:pattern_len]

            # Check for leading zeros
            if pattern[0] == '0':
                continue

            # Check if this pattern repeated makes the whole number
            repetitions = length // pattern_len
            if repetitions >= 2 and pattern * repetitions == num_str:
                return True

    return False


def solve_part1(input_file):
    """
    Find all invalid product IDs in the given ranges and sum them (Part 1 rules).
    """
    # Read the input file
    with open(input_file, 'r') as f:
        content = f.read().strip()

    # Parse the ranges
    ranges = []
    for range_str in content.split(','):
        range_str = range_str.strip()
        if range_str:
            start, end = range_str.split('-')
            ranges.append((int(start), int(end)))

    # Find all invalid IDs
    total = 0
    invalid_ids = []

    for start, end in ranges:
        for num in range(start, end + 1):
            if is_invalid_id_part1(num):
                invalid_ids.append(num)
                total += num

    return total, invalid_ids


def solve_part2(input_file):
    """
    Find all invalid product IDs in the given ranges and sum them (Part 2 rules).
    """
    # Read the input file
    with open(input_file, 'r') as f:
        content = f.read().strip()

    # Parse the ranges
    ranges = []
    for range_str in content.split(','):
        range_str = range_str.strip()
        if range_str:
            start, end = range_str.split('-')
            ranges.append((int(start), int(end)))

    # Find all invalid IDs
    total = 0
    invalid_ids = []

    for start, end in ranges:
        for num in range(start, end + 1):
            if is_invalid_id_part2(num):
                invalid_ids.append(num)
                total += num

    return total, invalid_ids


if __name__ == "__main__":
    print("Part 1:")
    result1, invalid_list1 = solve_part1("input.txt")
    print(f"Total sum of invalid IDs: {result1}")
    print(f"Number of invalid IDs found: {len(invalid_list1)}")

    print("\nPart 2:")
    result2, invalid_list2 = solve_part2("input.txt")
    print(f"Total sum of invalid IDs: {result2}")
    print(f"Number of invalid IDs found: {len(invalid_list2)}")
