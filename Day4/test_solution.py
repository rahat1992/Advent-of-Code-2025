import unittest
import os
from solution import count_adjacent_rolls, count_accessible_rolls, solve_part1, solve_part2, remove_accessible_rolls, count_total_removable_rolls


class TestPrintingDepartment(unittest.TestCase):

    def test_count_adjacent_rolls_corner(self):
        """Test counting adjacent rolls for a corner position."""
        grid = [
            "@@.",
            "@@.",
            "..."
        ]
        # Position (0, 0) has 3 adjacent rolls
        self.assertEqual(count_adjacent_rolls(grid, 0, 0), 3)

    def test_count_adjacent_rolls_center(self):
        """Test counting adjacent rolls for a center position."""
        grid = [
            "@@@",
            "@@@",
            "@@@"
        ]
        # Position (1, 1) has 8 adjacent rolls
        self.assertEqual(count_adjacent_rolls(grid, 1, 1), 8)

    def test_count_adjacent_rolls_edge(self):
        """Test counting adjacent rolls for an edge position."""
        grid = [
            "@@@",
            "@@@",
            "..."
        ]
        # Position (0, 1) has 5 adjacent rolls
        self.assertEqual(count_adjacent_rolls(grid, 0, 1), 5)

    def test_count_adjacent_rolls_isolated(self):
        """Test counting adjacent rolls for an isolated roll."""
        grid = [
            "...",
            ".@.",
            "..."
        ]
        # Position (1, 1) has 0 adjacent rolls
        self.assertEqual(count_adjacent_rolls(grid, 1, 1), 0)

    def test_count_adjacent_rolls_empty_position(self):
        """Test counting adjacent rolls for an empty position."""
        grid = [
            "@@@",
            "@.@",
            "@@@"
        ]
        # Position (1, 1) is empty but has 8 adjacent rolls
        self.assertEqual(count_adjacent_rolls(grid, 1, 1), 8)

    def test_count_adjacent_rolls_partial(self):
        """Test counting adjacent rolls with some adjacent positions."""
        grid = [
            ".@.",
            "@@@",
            ".@."
        ]
        # Position (1, 1) has 4 adjacent rolls
        self.assertEqual(count_adjacent_rolls(grid, 1, 1), 4)

    def test_count_accessible_rolls_example(self):
        """Test with the example from the problem."""
        grid = [
            "..@@.@@@@.",
            "@@@.@.@.@@",
            "@@@@@.@.@@",
            "@.@@@@..@.",
            "@@.@@@@.@@",
            ".@@@@@@@.@",
            ".@.@.@.@@@",
            "@.@@@.@@@@",
            ".@@@@@@@@.",
            "@.@.@@@.@."
        ]
        # The example states there are 13 accessible rolls
        self.assertEqual(count_accessible_rolls(grid), 13)

    def test_count_accessible_rolls_all_accessible(self):
        """Test when all rolls are accessible."""
        grid = [
            "@.@",
            "...",
            "@.@"
        ]
        # All 4 rolls have 0 adjacent rolls, so all are accessible
        self.assertEqual(count_accessible_rolls(grid), 4)

    def test_count_accessible_rolls_none_accessible(self):
        """Test when no rolls are accessible."""
        grid = [
            "@@@@@",
            "@@@@@",
            "@@@@@",
            "@@@@@",
            "@@@@@"
        ]
        # Interior rolls have 8 adjacent, edge rolls have 5, corner rolls have 3
        # All have >= 4 adjacent except corners (3 adjacent)
        # Corners: (0,0), (0,4), (4,0), (4,4) all have 3 adjacent, so accessible
        self.assertEqual(count_accessible_rolls(grid), 4)

    def test_count_accessible_rolls_single_roll(self):
        """Test with a single roll."""
        grid = [
            "...",
            ".@.",
            "..."
        ]
        # One roll with 0 adjacent rolls
        self.assertEqual(count_accessible_rolls(grid), 1)

    def test_count_accessible_rolls_two_rolls_adjacent(self):
        """Test with two adjacent rolls."""
        grid = [
            "...",
            ".@@",
            "..."
        ]
        # Both rolls have 1 adjacent roll each, so both are accessible
        self.assertEqual(count_accessible_rolls(grid), 2)

    def test_count_accessible_rolls_line(self):
        """Test with a line of rolls."""
        grid = [
            ".....",
            "@@@@@",
            "....."
        ]
        # Each roll has at most 2 adjacent rolls (left and right)
        # All 5 rolls are accessible
        self.assertEqual(count_accessible_rolls(grid), 5)

    def test_count_accessible_rolls_cross(self):
        """Test with a cross pattern."""
        grid = [
            "..@..",
            "..@..",
            "@@@@@",
            "..@..",
            "..@.."
        ]
        # Center (2,2) has 4 adjacent, not accessible
        # (1,2) has 4 adjacent, not accessible
        # (3,2) has 4 adjacent, not accessible
        # (2,1) has 4 adjacent, not accessible
        # (2,3) has 4 adjacent, not accessible
        # Only the 4 endpoints are accessible: (0,2), (2,0), (2,4), (4,2)
        self.assertEqual(count_accessible_rolls(grid), 4)

    def test_count_accessible_rolls_dense_cluster(self):
        """Test with a dense cluster."""
        grid = [
            "@@@@",
            "@@@@",
            "@@@@",
            "@@@@"
        ]
        # Only corners have < 4 adjacent (they have 3)
        # 4 corners are accessible
        self.assertEqual(count_accessible_rolls(grid), 4)

    def test_count_accessible_rolls_sparse(self):
        """Test with sparse rolls."""
        grid = [
            "@...@",
            ".....",
            "..@..",
            ".....",
            "@...@"
        ]
        # All 5 rolls are isolated, all accessible
        self.assertEqual(count_accessible_rolls(grid), 5)

    def test_count_accessible_rolls_boundary_3_adjacent(self):
        """Test rolls with exactly 3 adjacent (should be accessible)."""
        grid = [
            "@@.",
            "@@.",
            "..."
        ]
        # (0,0) has 3 adjacent, (0,1) has 2, (1,0) has 2, (1,1) has 3
        # All 4 are accessible
        self.assertEqual(count_accessible_rolls(grid), 4)

    def test_count_accessible_rolls_boundary_4_adjacent(self):
        """Test rolls with exactly 4 adjacent (should not be accessible)."""
        grid = [
            "@@@",
            "@@@",
            "..."
        ]
        # Center roll (0,1) has 5 adjacent, not accessible
        # (0,0) has 3, (0,2) has 3, (1,0) has 3, (1,1) has 5, (1,2) has 3
        # 4 accessible (the 4 corners of the 2x3 block)
        accessible = count_accessible_rolls(grid)
        # Actually: (0,0)=3, (0,1)=5, (0,2)=3, (1,0)=3, (1,1)=5, (1,2)=3
        # So 4 rolls with < 4 adjacent
        self.assertEqual(accessible, 4)

    def test_solve_part1_example_file(self):
        """Test Part 1 with the example input as a file."""
        test_file = "test_input.txt"
        example_input = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

        with open(test_file, 'w') as f:
            f.write(example_input)

        result = solve_part1(test_file)
        self.assertEqual(result, 13)

        os.remove(test_file)

    def test_actual_input_part1(self):
        """Test Part 1 with the actual input file."""
        if os.path.exists("input.txt"):
            result = solve_part1("input.txt")
            self.assertEqual(result, 1428)

    # Part 2 Tests
    def test_remove_accessible_rolls_simple(self):
        """Test removing accessible rolls from a simple grid."""
        grid = [
            "@.@",
            "...",
            "@.@"
        ]
        # All 4 rolls are accessible (0 adjacent each)
        new_grid, removed = remove_accessible_rolls(grid)
        self.assertEqual(removed, 4)
        # Grid should be all dots
        for row in new_grid:
            self.assertTrue(all(c == '.' for c in row))

    def test_remove_accessible_rolls_partial(self):
        """Test removing accessible rolls where some remain."""
        grid = [
            "@@.",
            "@@.",
            "..."
        ]
        # All 4 rolls have < 4 adjacent, so all should be removed
        new_grid, removed = remove_accessible_rolls(grid)
        self.assertEqual(removed, 4)

    def test_remove_accessible_rolls_none(self):
        """Test when no rolls can be removed."""
        grid = [
            "@@@@@",
            "@@@@@",
            "@@@@@",
            "@@@@@",
            "@@@@@"
        ]
        # Most rolls have >= 4 adjacent, only corners (3 adjacent) are accessible
        new_grid, removed = remove_accessible_rolls(grid)
        self.assertEqual(removed, 4)  # 4 corners

    def test_count_total_removable_rolls_example(self):
        """Test Part 2 with the example from the problem."""
        grid = [
            "..@@.@@@@.",
            "@@@.@.@.@@",
            "@@@@@.@.@@",
            "@.@@@@..@.",
            "@@.@@@@.@@",
            ".@@@@@@@.@",
            ".@.@.@.@@@",
            "@.@@@.@@@@",
            ".@@@@@@@@.",
            "@.@.@@@.@."
        ]
        # The example states 43 rolls can be removed in total
        self.assertEqual(count_total_removable_rolls(grid), 43)

    def test_count_total_removable_rolls_single_iteration(self):
        """Test when all rolls are removed in one iteration."""
        grid = [
            "@.@",
            "...",
            "@.@"
        ]
        # All 4 rolls removed in one pass
        self.assertEqual(count_total_removable_rolls(grid), 4)

    def test_count_total_removable_rolls_multiple_iterations(self):
        """Test when multiple iterations are needed."""
        grid = [
            "@@@@",
            "@@@@",
            "@@@@",
            "@@@@"
        ]
        # First pass removes 4 corners (each with 3 adjacent)
        # After that, remaining rolls form a dense cluster where all have >= 4 adjacent
        result = count_total_removable_rolls(grid)
        # Only the 4 corners can be removed
        self.assertEqual(result, 4)

    def test_count_total_removable_rolls_line(self):
        """Test with a line of rolls."""
        grid = [
            ".....",
            "@@@@@",
            "....."
        ]
        # All 5 rolls have < 4 adjacent (at most 2), so all removed in one pass
        self.assertEqual(count_total_removable_rolls(grid), 5)

    def test_count_total_removable_rolls_empty(self):
        """Test with an empty grid."""
        grid = [
            ".....",
            ".....",
            "....."
        ]
        # No rolls to remove
        self.assertEqual(count_total_removable_rolls(grid), 0)

    def test_solve_part2_example_file(self):
        """Test Part 2 with the example input as a file."""
        test_file = "test_input_part2.txt"
        example_input = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""

        with open(test_file, 'w') as f:
            f.write(example_input)

        result = solve_part2(test_file)
        self.assertEqual(result, 43)

        os.remove(test_file)

    def test_actual_input_part2(self):
        """Test Part 2 with the actual input file."""
        if os.path.exists("input.txt"):
            result = solve_part2("input.txt")
            self.assertEqual(result, 8936)


if __name__ == "__main__":
    unittest.main(verbosity=2)
