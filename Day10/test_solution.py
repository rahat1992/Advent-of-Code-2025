import unittest
import os
from solution import (
    parse_input, parse_line, solve_part1, solve_part2,
    find_min_presses_dp, apply_buttons, state_to_int, button_to_int
)


class TestDay10(unittest.TestCase):

    def setUp(self):
        """Set up example input."""
        self.example_content = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
        self.test_file = "test_example.txt"
        with open(self.test_file, 'w') as f:
            f.write(self.example_content)

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_parse_line_machine1(self):
        """Test parsing the first machine."""
        line = '[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}'
        target, buttons, num_lights, joltage = parse_line(line)

        self.assertEqual(num_lights, 4)
        self.assertEqual(target, [False, True, True, False])
        self.assertEqual(len(buttons), 6)
        self.assertEqual(buttons[0], {3})
        self.assertEqual(buttons[1], {1, 3})
        self.assertEqual(buttons[5], {0, 1})
        self.assertEqual(joltage, [3, 5, 4, 7])

    def test_parse_line_machine2(self):
        """Test parsing the second machine."""
        line = '[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}'
        target, buttons, num_lights, joltage = parse_line(line)

        self.assertEqual(num_lights, 5)
        self.assertEqual(target, [False, False, False, True, False])
        self.assertEqual(len(buttons), 5)
        self.assertEqual(joltage, [7, 5, 12, 7, 2])

    def test_parse_line_machine3(self):
        """Test parsing the third machine."""
        line = '[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}'
        target, buttons, num_lights, joltage = parse_line(line)

        self.assertEqual(num_lights, 6)
        self.assertEqual(target, [False, True, True, True, False, True])
        self.assertEqual(len(buttons), 4)
        self.assertEqual(joltage, [10, 11, 11, 5, 10, 5])

    def test_apply_buttons(self):
        """Test button application logic."""
        num_lights = 6
        buttons = [{0}, {0, 3, 4}]

        # Press no buttons
        result = apply_buttons(num_lights, buttons, [False, False])
        self.assertEqual(result, [False, False, False, False, False, False])

        # Press first button
        result = apply_buttons(num_lights, buttons, [True, False])
        self.assertEqual(result, [True, False, False, False, False, False])

        # Press second button
        result = apply_buttons(num_lights, buttons, [False, True])
        self.assertEqual(result, [True, False, False, True, True, False])

        # Press both buttons (light 0 toggles twice = off)
        result = apply_buttons(num_lights, buttons, [True, True])
        self.assertEqual(result, [False, False, False, True, True, False])

    def test_state_to_int(self):
        """Test state to bitmask conversion."""
        self.assertEqual(state_to_int([False, False, False]), 0)
        self.assertEqual(state_to_int([True, False, False]), 1)
        self.assertEqual(state_to_int([False, True, False]), 2)
        self.assertEqual(state_to_int([True, True, False]), 3)
        self.assertEqual(state_to_int([True, True, True]), 7)

    def test_button_to_int(self):
        """Test button set to bitmask conversion."""
        self.assertEqual(button_to_int({0}, 4), 1)
        self.assertEqual(button_to_int({1}, 4), 2)
        self.assertEqual(button_to_int({0, 1}, 4), 3)
        self.assertEqual(button_to_int({0, 2}, 4), 5)

    def test_find_min_presses_machine1(self):
        """Test minimum presses for first machine."""
        line = '[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}'
        target, buttons, num_lights, _ = parse_line(line)
        result = find_min_presses_dp(target, buttons, num_lights)
        self.assertEqual(result, 2)

    def test_find_min_presses_machine2(self):
        """Test minimum presses for second machine."""
        line = '[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}'
        target, buttons, num_lights, _ = parse_line(line)
        result = find_min_presses_dp(target, buttons, num_lights)
        self.assertEqual(result, 3)

    def test_find_min_presses_machine3(self):
        """Test minimum presses for third machine."""
        line = '[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}'
        target, buttons, num_lights, _ = parse_line(line)
        result = find_min_presses_dp(target, buttons, num_lights)
        self.assertEqual(result, 2)

    def test_solve_part1_example(self):
        """Test Part 1 with the example from the problem."""
        result = solve_part1(self.test_file)
        self.assertEqual(result, 7)

    def test_solve_part1_single_button(self):
        """Test with a single button that solves it."""
        test_file = "test_single.txt"
        with open(test_file, 'w') as f:
            f.write('[#.] (0) {1}')

        result = solve_part1(test_file)
        self.assertEqual(result, 1)

        os.remove(test_file)

    def test_solve_part1_no_presses_needed(self):
        """Test when target is all off (no presses needed)."""
        test_file = "test_zero.txt"
        with open(test_file, 'w') as f:
            f.write('[...] (0) (1) (2) {1,2,3}')

        result = solve_part1(test_file)
        self.assertEqual(result, 0)

        os.remove(test_file)

    def test_actual_input_part1(self):
        """Test Part 1 with the actual input file."""
        if os.path.exists("input.txt"):
            result = solve_part1("input.txt")
            print(f"\nPart 1 result: {result}")
            self.assertIsInstance(result, int)
            self.assertGreater(result, 0)

    def test_solve_part2_example(self):
        """Test Part 2 with the example from the problem."""
        result = solve_part2(self.test_file)
        self.assertEqual(result, 33)

    @unittest.skip("Part 2 takes several minutes on actual input")
    def test_actual_input_part2(self):
        """Test Part 2 with the actual input file."""
        if os.path.exists("input.txt"):
            result = solve_part2("input.txt")
            print(f"\nPart 2 result: {result}")
            self.assertIsInstance(result, int)
            self.assertEqual(result, 21111)


if __name__ == "__main__":
    unittest.main(verbosity=2)
