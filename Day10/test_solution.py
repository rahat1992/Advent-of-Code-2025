import unittest
import os
from solution import parse_input, solve_part1, solve_part2


class TestDay10(unittest.TestCase):

    def test_parse_input(self):
        """Test input parsing."""
        # TODO: Add parsing tests
        pass

    def test_solve_part1_example(self):
        """Test Part 1 with the example from the problem."""
        # TODO: Add example test
        pass

    def test_solve_part2_example(self):
        """Test Part 2 with the example from the problem."""
        # TODO: Add example test
        pass

    def test_actual_input_part1(self):
        """Test Part 1 with the actual input file."""
        if os.path.exists("input.txt"):
            result = solve_part1("input.txt")
            print(f"\nPart 1 result: {result}")
            self.assertIsInstance(result, int)

    def test_actual_input_part2(self):
        """Test Part 2 with the actual input file."""
        if os.path.exists("input.txt"):
            result = solve_part2("input.txt")
            print(f"\nPart 2 result: {result}")
            self.assertIsInstance(result, int)


if __name__ == "__main__":
    unittest.main(verbosity=2)
