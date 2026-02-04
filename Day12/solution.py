def parse_input(input_file):
    with open(input_file, 'r') as f:
        lines = f.read().strip().split('\n')

    shapes = {}
    regions = []

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if ':' not in line:
            i += 1
            continue

        before_colon = line.split(':')[0].strip()

        if 'x' in before_colon:
            after_colon = line.split(':', 1)[1].strip()
            w, h = map(int, before_colon.split('x'))
            counts = list(map(int, after_colon.split()))
            regions.append((w, h, counts))
            i += 1
        elif before_colon.isdigit():
            idx = int(before_colon)
            i += 1
            cells = set()
            r = 0
            while i < len(lines) and lines[i].strip() and ':' not in lines[i]:
                for c, ch in enumerate(lines[i]):
                    if ch == '#':
                        cells.add((r, c))
                r += 1
                i += 1
            shapes[idx] = frozenset(cells)
        else:
            i += 1

    return shapes, regions


def normalize(cells):
    min_r = min(r for r, c in cells)
    min_c = min(c for r, c in cells)
    return frozenset((r - min_r, c - min_c) for r, c in cells)


def get_orientations(cells):
    orientations = set()
    current = set(cells)
    for _ in range(4):
        orientations.add(normalize(current))
        orientations.add(normalize({(r, -c) for r, c in current}))
        current = {(c, -r) for r, c in current}
    return [sorted(o) for o in orientations]


def solve_region_backtrack(width, height, shape_counts, all_orientations):
    """Backtracking solver for small grids."""
    grid_area = width * height

    total_pieces_area = 0
    for i, c in enumerate(shape_counts):
        if c > 0 and i in all_orientations:
            total_pieces_area += c * len(all_orientations[i][0])

    if total_pieces_area == 0:
        return True
    if total_pieces_area > grid_area:
        return False

    must_cover_all = (total_pieces_area == grid_area)
    remaining = list(shape_counts)

    cell_placements = [[] for _ in range(grid_area)]

    for shape_idx in range(len(shape_counts)):
        if shape_counts[shape_idx] == 0:
            continue
        for orientation in all_orientations[shape_idx]:
            max_r = max(r for r, c in orientation)
            max_c = max(c for r, c in orientation)
            piece_area = len(orientation)
            for r in range(height - max_r):
                for c in range(width - max_c):
                    mask = 0
                    min_bit = grid_area
                    for cr, cc in orientation:
                        bit = (cr + r) * width + (cc + c)
                        mask |= 1 << bit
                        min_bit = min(min_bit, bit)
                    cell_placements[min_bit].append((shape_idx, mask, piece_area))

    def backtrack(grid, remaining_area, start):
        if remaining_area == 0:
            return True

        for cell in range(start, grid_area):
            if grid & (1 << cell):
                continue

            for shape_idx, mask, piece_area in cell_placements[cell]:
                if remaining[shape_idx] <= 0:
                    continue
                if (grid & mask) == 0:
                    remaining[shape_idx] -= 1
                    if backtrack(grid | mask, remaining_area - piece_area, cell + 1):
                        remaining[shape_idx] += 1
                        return True
                    remaining[shape_idx] += 1

            if must_cover_all:
                return False

        return remaining_area == 0

    return backtrack(0, total_pieces_area, 0)


def solve_part1(input_file):
    shapes, regions = parse_input(input_file)

    all_orientations = {}
    max_box_size = 0
    for idx, cells in shapes.items():
        orientations = get_orientations(cells)
        all_orientations[idx] = orientations
        for ori in orientations:
            h = max(r for r, c in ori) + 1
            w = max(c for r, c in ori) + 1
            max_box_size = max(max_box_size, h, w)

    count = 0
    for width, height, shape_counts in regions:
        total_pieces = sum(shape_counts)
        total_area = sum(
            c * len(all_orientations[i][0])
            for i, c in enumerate(shape_counts) if c > 0 and i in all_orientations
        )
        grid_area = width * height

        if total_area > grid_area:
            continue

        if total_area == 0:
            count += 1
            continue

        # Fast path: each piece fits in a max_box_size x max_box_size box.
        # If we can tile the grid with non-overlapping boxes, each piece gets one.
        bs = max_box_size
        max_boxes = max(
            (width // bs) * (height // bs),
            (width // bs) * (height // bs),
        )
        if total_pieces <= max_boxes:
            count += 1
            continue

        # Slow path: backtracking for small/tight cases
        if solve_region_backtrack(width, height, shape_counts, all_orientations):
            count += 1

    return count


def solve_part2(input_file):
    return 0


if __name__ == "__main__":
    print("Part 1:")
    result1 = solve_part1("input.txt")
    print(f"Result: {result1}")

    print("\nPart 2:")
    result2 = solve_part2("input.txt")
    print(f"Result: {result2}")
