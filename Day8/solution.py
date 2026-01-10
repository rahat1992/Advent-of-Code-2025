import math
from collections import defaultdict


def parse_junction_boxes(input_file):
    """
    Parse the input file to get junction box positions.
    Returns a list of (x, y, z) tuples.
    """
    junction_boxes = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                x, y, z = map(int, line.split(','))
                junction_boxes.append((x, y, z))
    return junction_boxes


def distance(box1, box2):
    """
    Calculate the Euclidean distance between two junction boxes.
    """
    x1, y1, z1 = box1
    x2, y2, z2 = box2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)


class UnionFind:
    """
    Union-Find data structure for tracking connected components (circuits).
    """
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n

    def find(self, x):
        """Find the root of the set containing x with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """
        Unite the sets containing x and y.
        Returns True if they were in different sets, False otherwise.
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
        else:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
            self.rank[root_x] += 1

        return True

    def get_component_sizes(self):
        """
        Get the sizes of all connected components.
        Returns a list of sizes.
        """
        component_sizes = defaultdict(int)
        for i in range(len(self.parent)):
            root = self.find(i)
            component_sizes[root] = self.size[root]

        return list(component_sizes.values())


def solve_part1(input_file, num_pairs=1000):
    """
    Solve Part 1: Try to connect the num_pairs closest pairs of junction boxes.
    """
    junction_boxes = parse_junction_boxes(input_file)
    n = len(junction_boxes)

    # Create all possible edges with their distances
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(junction_boxes[i], junction_boxes[j])
            edges.append((dist, i, j))

    # Sort edges by distance
    edges.sort()

    # Use Union-Find to connect junction boxes
    # Try to connect the num_pairs closest pairs (some may already be connected)
    uf = UnionFind(n)

    for pair_idx in range(min(num_pairs, len(edges))):
        dist, i, j = edges[pair_idx]
        # Try to connect i and j (may or may not succeed if already connected)
        uf.union(i, j)

    # Get component sizes
    component_sizes = uf.get_component_sizes()

    # Sort in descending order and multiply the top 3
    component_sizes.sort(reverse=True)

    if len(component_sizes) >= 3:
        result = component_sizes[0] * component_sizes[1] * component_sizes[2]
    else:
        result = 1
        for size in component_sizes:
            result *= size

    return result


def solve_part2(input_file):
    """
    Solve Part 2: Connect boxes until all are in one circuit.
    Return the product of X coordinates of the last two boxes connected.
    """
    junction_boxes = parse_junction_boxes(input_file)
    n = len(junction_boxes)

    # Create all possible edges with their distances
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(junction_boxes[i], junction_boxes[j])
            edges.append((dist, i, j))

    # Sort edges by distance
    edges.sort()

    # Use Union-Find to connect junction boxes
    uf = UnionFind(n)
    num_components = n  # Start with n separate components

    last_connection = None

    for dist, i, j in edges:
        # Try to connect i and j
        if uf.union(i, j):
            num_components -= 1
            last_connection = (i, j)

            # Stop when all boxes are in one circuit
            if num_components == 1:
                break

    # Get the X coordinates of the last two boxes connected
    if last_connection:
        i, j = last_connection
        x1 = junction_boxes[i][0]
        x2 = junction_boxes[j][0]
        return x1 * x2

    return 0


if __name__ == "__main__":
    print("Part 1:")
    result1 = solve_part1("input.txt", num_pairs=1000)
    print(f"Product of three largest circuits: {result1}")

    print("\nPart 2:")
    result2 = solve_part2("input.txt")
    print(f"Product of X coordinates: {result2}")
