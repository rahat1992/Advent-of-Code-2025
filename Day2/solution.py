def is_invalid_id(num):
    """
    Check if a number is an invalid ID.
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


def solve_part1(input_file):
    """
    Find all invalid product IDs in the given ranges and sum them.
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
            if is_invalid_id(num):
                invalid_ids.append(num)
                total += num

    return total, invalid_ids


if __name__ == "__main__":
    result, invalid_list = solve_part1("input.txt")
    print(f"Total sum of invalid IDs: {result}")
    print(f"Number of invalid IDs found: {len(invalid_list)}")
