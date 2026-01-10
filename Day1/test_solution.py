import unittest
import os
from solution import solve_part1, solve_part2


class TestSafeSolution(unittest.TestCase):

    def setUp(self):
        """Create a test input file with the example from the problem."""
        self.test_file = "test_input.txt"
        with open(self.test_file, 'w') as f:
            f.write("L68\n")
            f.write("L30\n")
            f.write("R48\n")
            f.write("L5\n")
            f.write("R60\n")
            f.write("L55\n")
            f.write("L1\n")
            f.write("L99\n")
            f.write("R14\n")
            f.write("L82\n")

    def tearDown(self):
        """Clean up test file."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_part1_example(self):
        """Test Part 1 with the example from the problem.

        Expected sequence:
        - Start: 50
        - L68 -> 82
        - L30 -> 52
        - R48 -> 0 (count: 1)
        - L5 -> 95
        - R60 -> 55
        - L55 -> 0 (count: 2)
        - L1 -> 99
        - L99 -> 0 (count: 3)
        - R14 -> 14
        - L82 -> 32

        Total: 3 times ending at 0
        """
        result = solve_part1(self.test_file)
        self.assertEqual(result, 3)

    def test_part2_example(self):
        """Test Part 2 with the example from the problem.

        Expected: 6 times passing through 0
        - L68: passes through 0 once during rotation
        - L30: no pass through 0
        - R48: ends at 0 (count: 1)
        - L5: no pass through 0
        - R60: passes through 0 once during rotation
        - L55: ends at 0 (count: 1)
        - L1: no pass through 0
        - L99: ends at 0 (count: 1)
        - R14: no pass through 0
        - L82: passes through 0 once during rotation

        Total: 6 times
        """
        result = solve_part2(self.test_file)
        self.assertEqual(result, 6)

    def test_part1_single_rotation_to_zero(self):
        """Test a single rotation that ends at 0."""
        test_file = "test_single.txt"
        with open(test_file, 'w') as f:
            f.write("R50\n")  # 50 + 50 = 100 % 100 = 0

        result = solve_part1(test_file)
        self.assertEqual(result, 1)
        os.remove(test_file)

    def test_part1_no_zeros(self):
        """Test rotations that never end at 0."""
        test_file = "test_no_zeros.txt"
        with open(test_file, 'w') as f:
            f.write("R10\n")  # 50 + 10 = 60
            f.write("L5\n")   # 60 - 5 = 55

        result = solve_part1(test_file)
        self.assertEqual(result, 0)
        os.remove(test_file)

    def test_part2_multiple_cycles(self):
        """Test Part 2 with a rotation that goes through 0 multiple times.

        From the problem: "if the dial were pointing at 50, a single rotation
        like R1000 would cause the dial to point at 0 ten times"
        """
        test_file = "test_cycles.txt"
        with open(test_file, 'w') as f:
            f.write("R1000\n")  # Should pass through 0 ten times

        result = solve_part2(test_file)
        self.assertEqual(result, 10)
        os.remove(test_file)

    def test_part2_left_wrap_around(self):
        """Test Part 2 with left rotation that wraps around through 0."""
        test_file = "test_left_wrap.txt"
        with open(test_file, 'w') as f:
            # Start at 50, rotate L55 should pass through 0 once
            # 50 -> 49 -> ... -> 1 -> 0 -> 99 -> 98 -> 97 -> 96 -> 95
            f.write("L55\n")

        result = solve_part2(test_file)
        self.assertEqual(result, 1)
        os.remove(test_file)

    def test_part2_right_wrap_around(self):
        """Test Part 2 with right rotation that wraps around through 0."""
        test_file = "test_right_wrap.txt"
        with open(test_file, 'w') as f:
            # Start at 50, rotate R55 should pass through 0 once
            # 50 -> 51 -> ... -> 99 -> 0 -> 1 -> ... -> 5
            f.write("R55\n")

        result = solve_part2(test_file)
        self.assertEqual(result, 1)
        os.remove(test_file)

    def test_part2_exactly_to_zero(self):
        """Test that landing exactly on 0 counts in Part 2."""
        test_file = "test_exact_zero.txt"
        with open(test_file, 'w') as f:
            f.write("R50\n")  # 50 + 50 = 0

        result = solve_part2(test_file)
        self.assertEqual(result, 1)
        os.remove(test_file)

    def test_position_wrap_left(self):
        """Test that left rotation wraps correctly from low numbers."""
        test_file = "test_wrap_left.txt"
        with open(test_file, 'w') as f:
            f.write("L50\n")  # Start at 50, go to 0
            f.write("L1\n")   # From 0, go to 99
            f.write("R99\n")  # From 99, go to 98 (no wrap)

        # Part 1: Should end at 0 once (first rotation)
        result1 = solve_part1(test_file)
        self.assertEqual(result1, 1)

        os.remove(test_file)

    def test_position_wrap_right(self):
        """Test that right rotation wraps correctly from high numbers."""
        test_file = "test_wrap_right.txt"
        with open(test_file, 'w') as f:
            f.write("R49\n")  # Start at 50, go to 99
            f.write("R1\n")   # From 99, go to 0

        # Part 1: Should end at 0 once (second rotation)
        result1 = solve_part1(test_file)
        self.assertEqual(result1, 1)

        # Part 2: Should count 0 once (second rotation)
        result2 = solve_part2(test_file)
        self.assertEqual(result2, 1)

        os.remove(test_file)

    def test_empty_input(self):
        """Empty input file should return 0 for both parts."""
        test_file = "test_empty.txt"
        with open(test_file, 'w') as f:
            pass

        result1 = solve_part1(test_file)
        result2 = solve_part2(test_file)
        self.assertEqual(result1, 0)
        self.assertEqual(result2, 0)
        os.remove(test_file)

    def test_part2_large_left_rotation_multiple_cycles(self):
        """Test Part 2 with a large left rotation that includes many full cycles."""
        test_file = "test_large_left.txt"
        with open(test_file, 'w') as f:
            # 1234 clicks left from 50: 12 full cycles, remainder 34 (no extra wrap), so 12 hits on 0.
            f.write("L1234\n")

        result = solve_part2(test_file)
        self.assertEqual(result, 12)
        os.remove(test_file)

    def test_actual_input_part1(self):
        """Test Part 1 with the actual input file."""
        if os.path.exists("input.txt"):
            result = solve_part1("input.txt")
            self.assertEqual(result, 1011)

    def test_actual_input_part2(self):
        """Test Part 2 with the actual input file."""
        if os.path.exists("input.txt"):
            result = solve_part2("input.txt")
            self.assertEqual(result, 5967)


if __name__ == "__main__":
    unittest.main(verbosity=2)
