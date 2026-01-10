import unittest
import os
from solution import parse_manifold, simulate_beams, solve_part1, solve_part2


class TestLaboratories(unittest.TestCase):

    def test_parse_manifold_simple(self):
        """Test parsing a simple manifold."""
        test_file = "test_parse.txt"
        content = """...S...
.......
...^..."""

        with open(test_file, 'w') as f:
            f.write(content)

        grid, start_row, start_col = parse_manifold(test_file)

        self.assertEqual(start_row, 0)
        self.assertEqual(start_col, 3)
        self.assertEqual(len(grid), 3)

        os.remove(test_file)

    def test_simulate_beams_single_split(self):
        """Test simulation with a single splitter."""
        test_file = "test_single.txt"
        content = """...S...
.......
...^..."""

        with open(test_file, 'w') as f:
            f.write(content)

        grid, start_row, start_col = parse_manifold(test_file)
        splits = simulate_beams(grid, start_row, start_col)

        # Should split once
        self.assertEqual(splits, 1)

        os.remove(test_file)

    def test_simulate_beams_no_splitters(self):
        """Test simulation with no splitters."""
        test_file = "test_no_split.txt"
        content = """...S...
.......
......."""

        with open(test_file, 'w') as f:
            f.write(content)

        grid, start_row, start_col = parse_manifold(test_file)
        splits = simulate_beams(grid, start_row, start_col)

        # No splits
        self.assertEqual(splits, 0)

        os.remove(test_file)

    def test_simulate_beams_two_splitters_side_by_side(self):
        """Test two splitters side by side."""
        test_file = "test_two_side.txt"
        content = """..S..
.....
..^.."""

        with open(test_file, 'w') as f:
            f.write(content)

        grid, start_row, start_col = parse_manifold(test_file)
        splits = simulate_beams(grid, start_row, start_col)

        # Beam goes straight down and hits the splitter
        self.assertEqual(splits, 1)

        os.remove(test_file)

    def test_simulate_beams_cascading(self):
        """Test cascading splitters."""
        test_file = "test_cascade.txt"
        content = """.S.
...
.^.
...
^.^"""

        with open(test_file, 'w') as f:
            f.write(content)

        grid, start_row, start_col = parse_manifold(test_file)
        splits = simulate_beams(grid, start_row, start_col)

        # First split at row 2, then two more splits at row 4
        self.assertEqual(splits, 3)

        os.remove(test_file)

    def test_simulate_beams_example(self):
        """Test with the example from the problem."""
        test_file = "test_example.txt"
        example = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""

        with open(test_file, 'w') as f:
            f.write(example)

        result = solve_part1(test_file)
        self.assertEqual(result, 21)

        os.remove(test_file)

    def test_solve_part1_single_row(self):
        """Test with just a starting position and one splitter."""
        test_file = "test_single_row.txt"
        content = """S
.
^"""

        with open(test_file, 'w') as f:
            f.write(content)

        result = solve_part1(test_file)
        self.assertEqual(result, 1)

        os.remove(test_file)

    def test_simulate_beams_beam_exits(self):
        """Test that beams properly exit the manifold."""
        test_file = "test_exit.txt"
        content = """.S.
...
..."""

        with open(test_file, 'w') as f:
            f.write(content)

        grid, start_row, start_col = parse_manifold(test_file)
        splits = simulate_beams(grid, start_row, start_col)

        # No splitters, beam just exits
        self.assertEqual(splits, 0)

        os.remove(test_file)

    def test_simulate_beams_multiple_paths_same_splitter(self):
        """Test cascading splits in a line."""
        test_file = "test_same_split.txt"
        content = """..S..
.....
..^..
.....
.^.^."""

        with open(test_file, 'w') as f:
            f.write(content)

        grid, start_row, start_col = parse_manifold(test_file)
        splits = simulate_beams(grid, start_row, start_col)

        # First split at (2,2), creating beams at (2,1) and (2,3)
        # Those beams continue and hit splitters at (4,1) and (4,3)
        # Total: 3 splits
        self.assertEqual(splits, 3)

        os.remove(test_file)

    def test_simulate_beams_edge_splitters(self):
        """Test splitters at the edges."""
        test_file = "test_edge.txt"
        content = """S....
.....
^...^"""

        with open(test_file, 'w') as f:
            f.write(content)

        grid, start_row, start_col = parse_manifold(test_file)
        splits = simulate_beams(grid, start_row, start_col)

        # Beam goes straight down, hits left edge splitter
        # Only creates one new beam (to the right)
        self.assertEqual(splits, 1)

        os.remove(test_file)

    def test_actual_input_part1(self):
        """Test Part 1 with the actual input file."""
        if os.path.exists("input.txt"):
            result = solve_part1("input.txt")
            self.assertEqual(result, 1672)

    def test_parse_manifold_finds_start(self):
        """Test that parsing correctly identifies S."""
        test_file = "test_find_s.txt"
        content = """.....
..S..
....."""

        with open(test_file, 'w') as f:
            f.write(content)

        grid, start_row, start_col = parse_manifold(test_file)

        self.assertEqual(start_row, 1)
        self.assertEqual(start_col, 2)

        os.remove(test_file)

    def test_simulate_beams_wide_manifold(self):
        """Test with a wider manifold."""
        test_file = "test_wide.txt"
        content = """.......S.......
...............
.......^......."""

        with open(test_file, 'w') as f:
            f.write(content)

        result = solve_part1(test_file)
        self.assertEqual(result, 1)

        os.remove(test_file)

    def test_simulate_beams_asymmetric_splits(self):
        """Test asymmetric splitter pattern."""
        test_file = "test_asym.txt"
        content = """....S....
.........
....^....
.........
...^.....
.........
..^......"""

        with open(test_file, 'w') as f:
            f.write(content)

        result = solve_part1(test_file)
        # First split at (2,4) creates beams at (2,3) and (2,5)
        # Beam at (2,3) hits splitter at (4,3), creating (4,2) and (4,4)
        # Beam at (4,2) hits splitter at (6,2), creating (6,1) and (6,3)
        # Total: 3 splits
        self.assertEqual(result, 3)

        os.remove(test_file)

    def test_quantum_particle_example(self):
        """Test Part 2 with the example from the problem."""
        test_file = "test_quantum_example.txt"
        example = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""

        with open(test_file, 'w') as f:
            f.write(example)

        result = solve_part2(test_file)
        self.assertEqual(result, 40)

        os.remove(test_file)

    def test_quantum_particle_no_splitters(self):
        """Test Part 2 with no splitters - should be 1 timeline."""
        test_file = "test_quantum_no_split.txt"
        content = """...S...
.......
.......
......."""

        with open(test_file, 'w') as f:
            f.write(content)

        result = solve_part2(test_file)
        self.assertEqual(result, 1)

        os.remove(test_file)

    def test_quantum_particle_single_split(self):
        """Test Part 2 with a single splitter - should be 2 timelines."""
        test_file = "test_quantum_single.txt"
        content = """...S...
.......
...^...
.......
......."""

        with open(test_file, 'w') as f:
            f.write(content)

        result = solve_part2(test_file)
        self.assertEqual(result, 2)

        os.remove(test_file)

    def test_quantum_particle_two_splitters(self):
        """Test Part 2 with two splitters in series."""
        test_file = "test_quantum_two.txt"
        content = """.S.
...
.^.
...
^.^"""

        with open(test_file, 'w') as f:
            f.write(content)

        result = solve_part2(test_file)
        # First split creates 2 paths at (2,0) and (2,2)
        # They hit edge splitters which redirect them both to (4,1)
        # So 2 paths converge and exit
        self.assertEqual(result, 2)

        os.remove(test_file)

    def test_quantum_particle_edge_splitter(self):
        """Test Part 2 with splitter at edge - only one branch possible."""
        test_file = "test_quantum_edge.txt"
        content = """S...
....
^..."""

        with open(test_file, 'w') as f:
            f.write(content)

        result = solve_part2(test_file)
        # Beam hits left edge splitter, only creates one new path (right)
        self.assertEqual(result, 1)

        os.remove(test_file)

    def test_actual_input_part2(self):
        """Test Part 2 with the actual input file."""
        if os.path.exists("input.txt"):
            result = solve_part2("input.txt")
            self.assertEqual(result, 231229866702355)


if __name__ == "__main__":
    unittest.main(verbosity=2)
