def parse_input(input_file):
    """
    Parse the input file to extract fresh ingredient ranges and available IDs.
    Returns: (list of (start, end) tuples, list of ingredient IDs)
    """
    with open(input_file, 'r') as f:
        content = f.read().strip()

    # Split by blank line
    parts = content.split('\n\n')

    # Parse ranges
    ranges = []
    for line in parts[0].split('\n'):
        if line.strip():
            start, end = line.strip().split('-')
            ranges.append((int(start), int(end)))

    # Parse ingredient IDs
    ingredient_ids = []
    for line in parts[1].split('\n'):
        if line.strip():
            ingredient_ids.append(int(line.strip()))

    return ranges, ingredient_ids


def is_fresh(ingredient_id, ranges):
    """
    Check if an ingredient ID is fresh (falls within any range).
    """
    for start, end in ranges:
        if start <= ingredient_id <= end:
            return True
    return False


def count_fresh_ingredients(ranges, ingredient_ids):
    """
    Count how many of the available ingredient IDs are fresh.
    """
    fresh_count = 0
    for ingredient_id in ingredient_ids:
        if is_fresh(ingredient_id, ranges):
            fresh_count += 1
    return fresh_count


def merge_ranges(ranges):
    """
    Merge overlapping ranges into non-overlapping ranges.
    Returns a list of merged (start, end) tuples.
    """
    if not ranges:
        return []

    # Sort ranges by start position
    sorted_ranges = sorted(ranges)

    merged = [sorted_ranges[0]]

    for current_start, current_end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]

        # Check if current range overlaps with the last merged range
        if current_start <= last_end + 1:
            # Merge by extending the end of the last range
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            # No overlap, add as a new range
            merged.append((current_start, current_end))

    return merged


def count_total_fresh_ids(ranges):
    """
    Count the total number of ingredient IDs that are considered fresh.
    This counts all IDs within all ranges (after merging overlaps).
    """
    merged = merge_ranges(ranges)

    total = 0
    for start, end in merged:
        # Count of IDs in this range (inclusive)
        total += end - start + 1

    return total


def solve_part1(input_file):
    """
    Solve Part 1: Count how many available ingredient IDs are fresh.
    """
    ranges, ingredient_ids = parse_input(input_file)
    fresh_count = count_fresh_ingredients(ranges, ingredient_ids)
    return fresh_count


def solve_part2(input_file):
    """
    Solve Part 2: Count the total number of ingredient IDs considered fresh
    by the ranges (regardless of available inventory).
    """
    ranges, _ = parse_input(input_file)
    total_fresh = count_total_fresh_ids(ranges)
    return total_fresh


if __name__ == "__main__":
    print("Part 1:")
    result1 = solve_part1("input.txt")
    print(f"Number of fresh ingredients: {result1}")

    print("\nPart 2:")
    result2 = solve_part2("input.txt")
    print(f"Total fresh ingredient IDs: {result2}")
