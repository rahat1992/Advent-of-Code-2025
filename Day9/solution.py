def parse_red_tiles(input_file):
    """
    Parse the input file to get red tile positions.
    Returns a list of (x, y) tuples.
    """
    red_tiles = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                x, y = map(int, line.split(','))
                red_tiles.append((x, y))
    return red_tiles


def calculate_rectangle_area(tile1, tile2):
    """
    Calculate the area of a rectangle with tile1 and tile2 as opposite corners.
    """
    x1, y1 = tile1
    x2, y2 = tile2
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    return width * height


def solve_part1(input_file):
    """
    Solve Part 1: Find largest rectangle using two red tiles as opposite corners.
    On a discrete grid, area = (width + 1) * (height + 1)
    """
    red_tiles = parse_red_tiles(input_file)

    max_area = 0

    # Check all pairs of red tiles as opposite corners
    for i in range(len(red_tiles)):
        for j in range(i + 1, len(red_tiles)):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[j]

            # Calculate rectangle area on discrete grid
            # Number of tiles = (max - min + 1) in each dimension
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height

            max_area = max(max_area, area)

    return max_area


def is_point_inside_polygon(x, y, vertices):
    """
    Check if point (x, y) is inside the polygon defined by vertices.
    Uses ray casting algorithm.
    """
    n = len(vertices)
    inside = False

    j = n - 1
    for i in range(n):
        xi, yi = vertices[i]
        xj, yj = vertices[j]

        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside

        j = i

    return inside


def get_green_tiles(red_tiles):
    """
    Get all green tiles: those on the boundary path and inside the polygon.
    Returns a set of (x, y) tuples.
    Only use for small examples - not efficient for large inputs.
    """
    green_tiles = set()

    # Add all tiles on the boundary (connecting consecutive red tiles)
    for i in range(len(red_tiles)):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[(i + 1) % len(red_tiles)]

        # Add all tiles between these two red tiles
        if x1 == x2:  # Vertical line
            min_y, max_y = min(y1, y2), max(y1, y2)
            for y in range(min_y, max_y + 1):
                green_tiles.add((x1, y))
        else:  # Horizontal line
            min_x, max_x = min(x1, x2), max(x1, x2)
            for x in range(min_x, max_x + 1):
                green_tiles.add((x, y1))

    # Find bounding box
    all_x = [t[0] for t in red_tiles]
    all_y = [t[1] for t in red_tiles]
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    # Add all tiles inside the polygon
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if is_point_inside_polygon(x, y, red_tiles):
                green_tiles.add((x, y))

    return green_tiles


def build_horizontal_segments(red_tiles):
    """
    Build a list of horizontal segments from the polygon edges.
    Returns list of (y, x_start, x_end) tuples.
    """
    segments = []
    for i in range(len(red_tiles)):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[(i + 1) % len(red_tiles)]
        if y1 == y2:  # Horizontal segment
            segments.append((y1, min(x1, x2), max(x1, x2)))
    return segments


def build_vertical_segments(red_tiles):
    """
    Build a list of vertical segments from the polygon edges.
    Returns list of (x, y_start, y_end) tuples.
    """
    segments = []
    for i in range(len(red_tiles)):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[(i + 1) % len(red_tiles)]
        if x1 == x2:  # Vertical segment
            segments.append((x1, min(y1, y2), max(y1, y2)))
    return segments


def compute_valid_ranges_at_y(y, vertical_segments, horizontal_segments, red_tiles):
    """
    Compute valid x-ranges at a specific y-coordinate.
    Returns list of (x_start, x_end) tuples.

    A tile at (x, y) is valid if it's:
    - On a horizontal segment at this y
    - On a vertical segment that includes this y
    - Inside the polygon
    """
    ranges = []

    # Add horizontal segments on this row (boundary)
    for seg_y, x_start, x_end in horizontal_segments:
        if seg_y == y:
            ranges.append((x_start, x_end))

    # Add vertical segments that touch this row (boundary)
    for x, y_start, y_end in vertical_segments:
        if y_start <= y <= y_end:
            ranges.append((x, x))

    # Find interior ranges using point-in-polygon for the x values that matter
    # Get all x-coordinates from vertical segments
    all_x = set()
    for x, y_start, y_end in vertical_segments:
        all_x.add(x)
    for seg_y, x_start, x_end in horizontal_segments:
        all_x.add(x_start)
        all_x.add(x_end)

    all_x = sorted(all_x)

    # Check interior between consecutive x values
    for i in range(len(all_x) - 1):
        x1, x2 = all_x[i], all_x[i + 1]
        if x2 > x1 + 1:
            # Check if the midpoint is inside the polygon
            mid_x = (x1 + x2) // 2
            if is_point_inside_polygon(mid_x, y, red_tiles):
                ranges.append((x1, x2))

    # Merge overlapping ranges
    if not ranges:
        return []

    ranges.sort()
    merged = [ranges[0]]
    for start, end in ranges[1:]:
        if start <= merged[-1][1] + 1:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))

    return merged


def compute_y_bands(red_tiles, vertical_segments, horizontal_segments):
    """
    Compute valid x-ranges for each y-coordinate that might be needed.
    Uses coordinate compression to avoid iterating over all y values.
    Returns dict mapping y -> list of valid (x_start, x_end) ranges.
    Also returns a sorted list of all critical y-coordinates.
    """
    # Critical y-coordinates where the polygon shape changes
    critical_ys = set()
    for x, y in red_tiles:
        critical_ys.add(y)

    critical_ys = sorted(critical_ys)

    bands = {}

    # Compute ranges for each critical y and the band below it
    for idx, y in enumerate(critical_ys):
        bands[y] = compute_valid_ranges_at_y(y, vertical_segments, horizontal_segments, red_tiles)

        # For the band between this y and the next critical y (exclusive)
        if idx < len(critical_ys) - 1:
            next_y = critical_ys[idx + 1]
            if next_y > y + 1:
                # Interior rows have the same ranges (determined by segments spanning across)
                test_y = y + 1
                interior_ranges = compute_valid_ranges_at_y(test_y, vertical_segments, horizontal_segments, red_tiles)
                # Store for all interior rows (we'll use lazy lookup)
                for interior_y in range(y + 1, next_y):
                    bands[interior_y] = interior_ranges

    return bands, critical_ys


def is_rectangle_valid(min_x, max_x, min_y, max_y, row_ranges):
    """
    Check if rectangle from (min_x, min_y) to (max_x, max_y) is fully valid.
    row_ranges is a dict mapping y -> list of valid (x_start, x_end) ranges.
    """
    for y in range(min_y, max_y + 1):
        if y not in row_ranges:
            return False
        # Check if [min_x, max_x] is fully contained in one of the ranges
        valid_for_row = False
        for x_start, x_end in row_ranges[y]:
            if x_start <= min_x and max_x <= x_end:
                valid_for_row = True
                break
        if not valid_for_row:
            return False
    return True


def is_rectangle_valid_fast(min_x, max_x, min_y, max_y, row_ranges, critical_ys):
    """
    Check if rectangle is fully valid, using band-based checking.
    Only checks at critical y-coordinates plus one representative from each band.
    """
    # Find critical ys within our range
    relevant_ys = []
    for y in critical_ys:
        if min_y <= y <= max_y:
            relevant_ys.append(y)

    # Add band representatives (mid-point between consecutive critical ys)
    for i in range(len(relevant_ys) - 1):
        y1, y2 = relevant_ys[i], relevant_ys[i + 1]
        if y2 > y1 + 1:
            relevant_ys.append(y1 + 1)  # Any interior point works

    # Also need to check edges if they're not at critical ys
    if min_y not in relevant_ys:
        relevant_ys.append(min_y)
    if max_y not in relevant_ys:
        relevant_ys.append(max_y)

    relevant_ys.sort()

    for y in relevant_ys:
        if y not in row_ranges:
            return False
        valid_for_row = False
        for x_start, x_end in row_ranges[y]:
            if x_start <= min_x and max_x <= x_end:
                valid_for_row = True
                break
        if not valid_for_row:
            return False

    return True


def solve_part2(input_file):
    """
    Solve Part 2: Find largest rectangle where all tiles are red or green.
    Uses coordinate compression for efficiency with large rectilinear polygons.
    """
    red_tiles = parse_red_tiles(input_file)

    # Build segment lists
    vertical_segments = build_vertical_segments(red_tiles)
    horizontal_segments = build_horizontal_segments(red_tiles)

    # Compute y-bands with valid x-ranges
    row_ranges, critical_ys = compute_y_bands(red_tiles, vertical_segments, horizontal_segments)

    max_area = 0

    # Check all pairs of red tiles as opposite corners
    for i in range(len(red_tiles)):
        for j in range(i + 1, len(red_tiles)):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[j]

            min_x, max_x = min(x1, x2), max(x1, x2)
            min_y, max_y = min(y1, y2), max(y1, y2)

            width = max_x - min_x + 1
            height = max_y - min_y + 1
            area = width * height

            # Skip if this can't beat current max
            if area <= max_area:
                continue

            # Check if rectangle is valid using fast band-based check
            if is_rectangle_valid_fast(min_x, max_x, min_y, max_y, row_ranges, critical_ys):
                max_area = area

    return max_area


if __name__ == "__main__":
    print("Part 1:")
    result1 = solve_part1("input.txt")
    print(f"Largest rectangle area: {result1}")

    print("\nPart 2:")
    result2 = solve_part2("input.txt")
    print(f"Largest rectangle area (red/green only): {result2}")
