def find_max_joltage_n_batteries(bank, n):
    """
    Find the maximum joltage possible from a bank by selecting exactly n batteries.

    Strategy: Greedy approach - at each position, decide whether to include this digit
    by looking ahead to find the best digit we can start with.
    """
    num_to_skip = len(bank) - n

    result = []
    start_idx = 0

    while len(result) < n:
        # How many more digits do we need?
        remaining_needed = n - len(result)

        # What's the furthest we can look ahead?
        # We need to leave enough digits after our choice to fill the remaining spots
        max_end = len(bank) - remaining_needed + 1

        # Find the maximum digit in the range [start_idx, max_end)
        best_digit = bank[start_idx]
        best_idx = start_idx

        for i in range(start_idx, max_end):
            if bank[i] > best_digit:
                best_digit = bank[i]
                best_idx = i

        # Add the best digit to result
        result.append(best_digit)

        # Move start index past the selected digit
        start_idx = best_idx + 1

    return int(''.join(result))


def find_max_joltage(bank):
    """
    Find the maximum joltage possible from a bank of batteries.
    We need to select exactly two batteries (digits) that form the largest number.
    """
    return find_max_joltage_n_batteries(bank, 2)


def solve_part1(input_file):
    """
    Find the maximum joltage from each bank (2 batteries) and sum them up.
    """
    with open(input_file, 'r') as f:
        banks = [line.strip() for line in f if line.strip()]

    total_joltage = 0
    max_joltages = []

    for bank in banks:
        max_joltage = find_max_joltage(bank)
        max_joltages.append(max_joltage)
        total_joltage += max_joltage

    return total_joltage, max_joltages


def solve_part2(input_file):
    """
    Find the maximum joltage from each bank (12 batteries) and sum them up.
    """
    with open(input_file, 'r') as f:
        banks = [line.strip() for line in f if line.strip()]

    total_joltage = 0
    max_joltages = []

    for bank in banks:
        max_joltage = find_max_joltage_n_batteries(bank, 12)
        max_joltages.append(max_joltage)
        total_joltage += max_joltage

    return total_joltage, max_joltages


if __name__ == "__main__":
    print("Part 1:")
    result1, joltages1 = solve_part1("input.txt")
    print(f"Total output joltage: {result1}")
    print(f"Number of banks: {len(joltages1)}")

    print("\nPart 2:")
    result2, joltages2 = solve_part2("input.txt")
    print(f"Total output joltage: {result2}")
    print(f"Number of banks: {len(joltages2)}")
