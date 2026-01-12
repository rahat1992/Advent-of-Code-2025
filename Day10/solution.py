import re
from itertools import combinations


def parse_line(line):
    """
    Parse a single machine specification line.
    Returns (target_state, buttons, num_lights, joltage_targets) where:
    - target_state is a list of booleans (True = on, False = off)
    - buttons is a list of sets, each set containing the light indices toggled by that button
    - num_lights is the number of indicator lights
    - joltage_targets is a list of integers (the joltage requirements)
    """
    # Extract indicator light diagram [...]
    diagram_match = re.search(r'\[([.#]+)\]', line)
    diagram = diagram_match.group(1)
    target_state = [c == '#' for c in diagram]
    num_lights = len(target_state)

    # Extract button wiring schematics (...)
    # Each button is a comma-separated list of indices
    button_matches = re.findall(r'\(([^)]+)\)', line)
    buttons = []
    for match in button_matches:
        indices = set(int(x) for x in match.split(','))
        buttons.append(indices)

    # Extract joltage requirements {...}
    joltage_match = re.search(r'\{([^}]+)\}', line)
    joltage_targets = [int(x) for x in joltage_match.group(1).split(',')]

    return target_state, buttons, num_lights, joltage_targets


def parse_input(input_file):
    """
    Parse the input file.
    Returns list of (target_state, buttons, num_lights, joltage_targets) tuples.
    """
    machines = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                machines.append(parse_line(line))
    return machines


def apply_buttons(num_lights, buttons, pressed):
    """
    Apply a set of button presses and return the resulting state.
    pressed is a list of booleans indicating which buttons are pressed.
    """
    state = [False] * num_lights
    for i, is_pressed in enumerate(pressed):
        if is_pressed:
            for light_idx in buttons[i]:
                state[light_idx] = not state[light_idx]
    return state


def find_min_presses_brute_force(target_state, buttons, num_lights):
    """
    Find minimum number of button presses using brute force.
    Since pressing a button twice cancels out, we only need 0 or 1 press per button.
    """
    num_buttons = len(buttons)

    # Try all combinations of buttons, starting with fewest
    for num_pressed in range(num_buttons + 1):
        for combo in combinations(range(num_buttons), num_pressed):
            pressed = [False] * num_buttons
            for idx in combo:
                pressed[idx] = True
            result = apply_buttons(num_lights, buttons, pressed)
            if result == target_state:
                return num_pressed

    # No solution found
    return float('inf')


def state_to_int(state):
    """Convert boolean state list to integer (bitmask)."""
    result = 0
    for i, val in enumerate(state):
        if val:
            result |= (1 << i)
    return result


def button_to_int(button_set, num_lights):
    """Convert button indices set to integer (bitmask)."""
    result = 0
    for idx in button_set:
        if idx < num_lights:
            result |= (1 << idx)
    return result


def find_min_presses_bitmask(target_state, buttons, num_lights):
    """
    Find minimum number of button presses using bitmask BFS.
    More efficient for larger numbers of lights.
    """
    target = state_to_int(target_state)
    button_masks = [button_to_int(b, num_lights) for b in buttons]
    num_buttons = len(buttons)

    # BFS to find minimum presses
    # State is (current_light_state, next_button_index)
    # We only try each button once (pressing twice cancels out)

    from collections import deque

    # dp[state] = minimum presses to reach that state
    # We use a dict since state space might be large
    best = {0: 0}  # Start with all lights off, 0 presses

    queue = deque([(0, 0, 0)])  # (light_state, button_index, num_presses)

    while queue:
        state, btn_idx, presses = queue.popleft()

        if state == target:
            return presses

        if btn_idx >= num_buttons:
            continue

        # Option 1: Don't press this button
        new_state1 = state
        if new_state1 not in best or best[new_state1] > presses:
            best[new_state1] = presses
            queue.append((new_state1, btn_idx + 1, presses))

        # Option 2: Press this button
        new_state2 = state ^ button_masks[btn_idx]
        if new_state2 not in best or best[new_state2] > presses + 1:
            best[new_state2] = presses + 1
            queue.append((new_state2, btn_idx + 1, presses + 1))

    return best.get(target, float('inf'))


def find_min_presses_dp(target_state, buttons, num_lights):
    """
    Find minimum number of button presses using dynamic programming.
    dp[i][state] = minimum presses using first i buttons to reach state
    """
    target = state_to_int(target_state)
    button_masks = [button_to_int(b, num_lights) for b in buttons]
    num_buttons = len(buttons)

    # dp[state] = minimum presses to reach that state
    dp = {0: 0}

    for btn_idx in range(num_buttons):
        new_dp = {}
        mask = button_masks[btn_idx]

        for state, presses in dp.items():
            # Option 1: Don't press this button
            if state not in new_dp or new_dp[state] > presses:
                new_dp[state] = presses

            # Option 2: Press this button
            new_state = state ^ mask
            if new_state not in new_dp or new_dp[new_state] > presses + 1:
                new_dp[new_state] = presses + 1

        dp = new_dp

    return dp.get(target, float('inf'))


def solve_part1(input_file):
    """
    Solve Part 1: Find minimum total button presses for all machines.
    """
    machines = parse_input(input_file)
    total_presses = 0

    for target_state, buttons, num_lights, _ in machines:
        min_presses = find_min_presses_dp(target_state, buttons, num_lights)
        if min_presses == float('inf'):
            # No solution - should not happen for valid input
            raise ValueError("No solution found for machine")
        total_presses += min_presses

    return total_presses


def solve_linear_system_min_sum(A, b):
    """
    Solve Ax = b for non-negative integers x, minimizing sum(x).
    A is a list of lists (rows), b is a list of targets.

    Uses Gaussian elimination to find the general solution, then
    searches for the minimum sum non-negative integer solution.

    Returns the minimum sum or float('inf') if no solution.
    """
    from fractions import Fraction

    m = len(A)  # number of equations (counters)
    n = len(A[0]) if A else 0  # number of variables (buttons)

    if n == 0:
        return 0 if all(bi == 0 for bi in b) else float('inf')

    # Convert to Fraction for exact arithmetic
    # Augmented matrix [A | b]
    aug = [[Fraction(A[i][j]) for j in range(n)] + [Fraction(b[i])] for i in range(m)]

    # Gaussian elimination with partial pivoting
    pivot_cols = []
    row = 0
    for col in range(n):
        # Find pivot
        pivot_row = None
        for r in range(row, m):
            if aug[r][col] != 0:
                pivot_row = r
                break

        if pivot_row is None:
            continue

        # Swap rows
        aug[row], aug[pivot_row] = aug[pivot_row], aug[row]
        pivot_cols.append(col)

        # Eliminate
        pivot_val = aug[row][col]
        for r in range(m):
            if r != row and aug[r][col] != 0:
                factor = aug[r][col] / pivot_val
                for c in range(n + 1):
                    aug[r][c] -= factor * aug[row][c]

        # Normalize pivot row
        for c in range(n + 1):
            aug[row][c] /= pivot_val

        row += 1
        if row >= m:
            break

    # Check for inconsistency (0 = nonzero)
    for r in range(row, m):
        if aug[r][n] != 0:
            return float('inf')

    # Free variables are those not in pivot_cols
    free_vars = [j for j in range(n) if j not in pivot_cols]

    # If no free variables, we have a unique solution
    if not free_vars:
        x = [Fraction(0)] * n
        for i, col in enumerate(pivot_cols):
            x[col] = aug[i][n]

        # Check if all are non-negative integers
        for xi in x:
            if xi < 0 or xi.denominator != 1:
                return float('inf')

        return sum(int(xi) for xi in x)

    # With free variables, we need to search for minimum sum solution
    # Express pivot variables in terms of free variables
    # x_pivot[i] = aug[i][n] - sum(aug[i][j] * x_free[j] for j in free_vars)

    # For small number of free variables, we can search
    num_free = len(free_vars)

    # Determine bounds for free variables
    # Each pivot variable must be >= 0, giving constraints on free vars
    # This is complex for many free vars; use heuristic search

    if num_free > 15:
        # Too many free vars, use greedy heuristic
        return find_min_joltage_heuristic_search(A, b)

    # Search over non-negative integer values of free variables
    # Use smarter bounds based on pivot constraints

    # For each free variable, compute bounds from pivot constraints
    # x_pivot[i] = c[i] - sum(coef[i][j] * x_free[j]) >= 0
    # This gives bounds on each free variable

    # Extract pivot coefficients
    pivot_constants = [aug[i][n] for i in range(len(pivot_cols))]
    free_coeffs = [[aug[i][fv] for fv in free_vars] for i in range(len(pivot_cols))]

    def compute_solution(free_vals):
        """Compute full solution from free variable values."""
        x = [Fraction(0)] * n
        for idx, fv in enumerate(free_vars):
            x[fv] = Fraction(free_vals[idx])
        for i, col in enumerate(pivot_cols):
            val = pivot_constants[i]
            for idx in range(num_free):
                val -= free_coeffs[i][idx] * free_vals[idx]
            x[col] = val
        return x

    def is_valid_solution(x):
        """Check if solution is valid (non-negative integers)."""
        for xi in x:
            if xi < 0 or xi.denominator != 1:
                return False
        return True

    def compute_bounds():
        """Compute upper bounds for each free variable."""
        bounds = []
        for fidx in range(num_free):
            max_val = float('inf')
            for i in range(len(pivot_cols)):
                coef = free_coeffs[i][fidx]
                const = pivot_constants[i]
                # const - coef * x_free[fidx] >= 0
                # If coef > 0: x_free[fidx] <= const / coef
                if coef > 0:
                    max_val = min(max_val, int(const / coef))
            if max_val == float('inf'):
                max_val = max(b) if b else 100
            bounds.append(max(0, max_val))
        return bounds

    # Compute reasonable bounds for free variables
    # We need: pivot_constant[i] - sum(coef[i][j] * x_free[j]) >= 0 for all i
    # And all values must be integers

    max_target = max(b) if b else 100

    # Upper bounds for search - use a reasonable default
    # The actual constraints are more complex due to interactions
    upper_bounds = [max_target * 2] * num_free

    best_sum = float('inf')

    # Try x_free = 0 first
    x = compute_solution([0] * num_free)
    if is_valid_solution(x):
        best_sum = sum(int(xi) for xi in x)

    # Search with pruning
    def search(idx, free_vals, current_free_sum):
        nonlocal best_sum

        if current_free_sum >= best_sum:
            return

        if idx == num_free:
            x = compute_solution(free_vals)
            if is_valid_solution(x):
                total = sum(int(xi) for xi in x)
                if total < best_sum:
                    best_sum = total
            return

        # For current free variable, try all valid values
        max_val = min(upper_bounds[idx], best_sum - current_free_sum)

        for val in range(max_val + 1):
            free_vals[idx] = val
            search(idx + 1, free_vals, current_free_sum + val)

    if num_free > 0:
        search(0, [0] * num_free, 0)

    return best_sum


def find_min_joltage_heuristic_search(A, b):
    """
    Heuristic search for minimum sum solution when exact methods fail.
    Uses a greedy approach: at each step, choose the button that
    makes the most progress toward the target per press.
    """
    m = len(A)
    n = len(A[0]) if A else 0

    # Current state
    current = [0] * m
    target = list(b)
    presses = [0] * n
    total_presses = 0

    # Greedy: repeatedly find the best button to press
    max_iterations = sum(target) * 2  # Safeguard

    for _ in range(max_iterations):
        if current == target:
            return total_presses

        # Find the best button to press
        best_button = -1
        best_score = -1

        for j in range(n):
            # Check if pressing button j is valid (doesn't exceed any target)
            can_press = True
            progress = 0
            for i in range(m):
                new_val = current[i] + A[i][j]
                if new_val > target[i]:
                    can_press = False
                    break
                if A[i][j] > 0 and current[i] < target[i]:
                    progress += 1

            if can_press and progress > best_score:
                best_score = progress
                best_button = j

        if best_button == -1:
            # No valid button to press, stuck
            return float('inf')

        # Press the best button
        for i in range(m):
            current[i] += A[best_button][i]
        presses[best_button] += 1
        total_presses += 1

    return float('inf')


def find_min_joltage_presses_exact(buttons, joltage_targets):
    """
    Find minimum button presses using exact linear algebra.
    """
    num_buttons = len(buttons)
    num_counters = len(joltage_targets)

    # Build the constraint matrix A
    A = [[0] * num_buttons for _ in range(num_counters)]
    for j, button in enumerate(buttons):
        for counter_idx in button:
            if counter_idx < num_counters:
                A[counter_idx][j] = 1

    return solve_linear_system_min_sum(A, joltage_targets)


def find_min_joltage_presses_dp(buttons, joltage_targets):
    """
    Find minimum button presses using dynamic programming.
    State is a tuple of current counter values.
    """
    num_counters = len(joltage_targets)
    target = tuple(joltage_targets)

    # BFS from (0, 0, ..., 0) to target
    from collections import deque

    start = tuple([0] * num_counters)
    if start == target:
        return 0

    # visited[state] = minimum presses to reach that state
    visited = {start: 0}
    queue = deque([(start, 0)])

    # Precompute button effects as tuples
    button_effects = []
    for button in buttons:
        effect = [0] * num_counters
        for idx in button:
            if idx < num_counters:
                effect[idx] = 1
        button_effects.append(tuple(effect))

    max_target = max(joltage_targets)

    while queue:
        state, presses = queue.popleft()

        if presses > visited.get(state, float('inf')):
            continue

        for effect in button_effects:
            new_state = tuple(s + e for s, e in zip(state, effect))

            # Prune: don't exceed any target
            if any(ns > t for ns, t in zip(new_state, joltage_targets)):
                continue

            if new_state == target:
                return presses + 1

            if new_state not in visited or visited[new_state] > presses + 1:
                visited[new_state] = presses + 1
                queue.append((new_state, presses + 1))

    return float('inf')


def find_min_joltage_presses_greedy(buttons, joltage_targets):
    """
    Find minimum button presses using exact linear algebra approach.
    """
    return find_min_joltage_presses_exact(buttons, joltage_targets)


def solve_part2(input_file):
    """
    Solve Part 2: Find minimum total button presses to configure joltage counters.
    """
    machines = parse_input(input_file)
    total_presses = 0

    for _, buttons, _, joltage_targets in machines:
        min_presses = find_min_joltage_presses_greedy(buttons, joltage_targets)
        if min_presses == float('inf'):
            raise ValueError("No solution found for machine")
        total_presses += min_presses

    return total_presses


if __name__ == "__main__":
    print("Part 1:")
    result1 = solve_part1("input.txt")
    print(f"Result: {result1}")

    print("\nPart 2:")
    result2 = solve_part2("input.txt")
    print(f"Result: {result2}")
