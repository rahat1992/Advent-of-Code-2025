import re
from itertools import combinations


def parse_line(line):
    """
    Parse a single machine specification line.
    Returns (target_state, buttons) where:
    - target_state is a list of booleans (True = on, False = off)
    - buttons is a list of sets, each set containing the light indices toggled by that button
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

    return target_state, buttons, num_lights


def parse_input(input_file):
    """
    Parse the input file.
    Returns list of (target_state, buttons, num_lights) tuples.
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

    for target_state, buttons, num_lights in machines:
        min_presses = find_min_presses_dp(target_state, buttons, num_lights)
        if min_presses == float('inf'):
            # No solution - should not happen for valid input
            raise ValueError("No solution found for machine")
        total_presses += min_presses

    return total_presses


def solve_part2(input_file):
    """
    Solve Part 2.
    """
    machines = parse_input(input_file)
    # TODO: Implement when Part 2 is revealed
    return 0


if __name__ == "__main__":
    print("Part 1:")
    result1 = solve_part1("input.txt")
    print(f"Result: {result1}")

    print("\nPart 2:")
    result2 = solve_part2("input.txt")
    print(f"Result: {result2}")
