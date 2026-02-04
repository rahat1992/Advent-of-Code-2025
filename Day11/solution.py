from functools import lru_cache


def parse_input(input_file):
    """
    Parse the input file and build a directed graph.
    Returns a dictionary mapping each device to its list of outputs.
    """
    graph = {}
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(': ')
            device = parts[0]
            outputs = parts[1].split() if len(parts) > 1 else []
            graph[device] = outputs
    return graph


def count_paths(graph, start, end):
    """
    Count all paths from start to end in the directed graph.
    Uses memoization for efficiency.
    """
    @lru_cache(maxsize=None)
    def dfs(node):
        if node == end:
            return 1
        if node not in graph:
            return 0
        total = 0
        for neighbor in graph[node]:
            total += dfs(neighbor)
        return total

    return dfs(start)


def solve_part1(input_file):
    """
    Solve Part 1: Count all paths from 'you' to 'out'.
    """
    graph = parse_input(input_file)
    return count_paths(graph, 'you', 'out')


def count_paths_through_required(graph, start, end, required_nodes):
    """
    Count all paths from start to end that visit ALL required nodes.
    Uses memoization with state tracking for which required nodes have been visited.
    """
    required_set = frozenset(required_nodes)

    @lru_cache(maxsize=None)
    def dfs(node, visited_required):
        # Update visited_required if current node is one of the required ones
        if node in required_set:
            visited_required = visited_required | frozenset([node])

        if node == end:
            # Only count this path if all required nodes were visited
            return 1 if visited_required == required_set else 0

        if node not in graph:
            return 0

        total = 0
        for neighbor in graph[node]:
            total += dfs(neighbor, visited_required)
        return total

    return dfs(start, frozenset())


def solve_part2(input_file):
    """
    Solve Part 2: Count paths from 'svr' to 'out' that visit both 'dac' and 'fft'.
    """
    graph = parse_input(input_file)
    return count_paths_through_required(graph, 'svr', 'out', ['dac', 'fft'])


if __name__ == "__main__":
    print("Part 1:")
    result1 = solve_part1("input.txt")
    print(f"Result: {result1}")

    print("\nPart 2:")
    result2 = solve_part2("input.txt")
    print(f"Result: {result2}")
