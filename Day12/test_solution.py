import unittest
import os
from solution import parse_input, get_orientations, normalize, solve_region_backtrack, solve_part1


EXAMPLE = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""


class TestDay12(unittest.TestCase):

    def setUp(self):
        self.test_file = "test_example.txt"
        with open(self.test_file, 'w') as f:
            f.write(EXAMPLE)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_parse_shapes(self):
        shapes, regions = parse_input(self.test_file)
        self.assertEqual(len(shapes), 6)
        # Shape 4 should have 7 cells
        self.assertEqual(len(shapes[4]), 7)
        # Shape 0 should have 7 cells
        self.assertEqual(len(shapes[0]), 7)

    def test_parse_regions(self):
        shapes, regions = parse_input(self.test_file)
        self.assertEqual(len(regions), 3)
        self.assertEqual(regions[0], (4, 4, [0, 0, 0, 0, 2, 0]))
        self.assertEqual(regions[1], (12, 5, [1, 0, 1, 0, 2, 2]))
        self.assertEqual(regions[2], (12, 5, [1, 0, 1, 0, 3, 2]))

    def test_orientations(self):
        # A square shape should have only 1 orientation
        square = frozenset({(0, 0), (0, 1), (1, 0), (1, 1)})
        self.assertEqual(len(get_orientations(square)), 1)

    def test_region1_fits(self):
        """4x4 with two shape-4 pieces should fit."""
        shapes, regions = parse_input(self.test_file)
        all_orientations = {i: get_orientations(c) for i, c in shapes.items()}
        w, h, counts = regions[0]
        self.assertTrue(solve_region_backtrack(w, h, counts, all_orientations))

    def test_region2_fits(self):
        """12x5 with [1,0,1,0,2,2] should fit."""
        shapes, regions = parse_input(self.test_file)
        all_orientations = {i: get_orientations(c) for i, c in shapes.items()}
        w, h, counts = regions[1]
        self.assertTrue(solve_region_backtrack(w, h, counts, all_orientations))

    def test_region3_no_fit(self):
        """12x5 with [1,0,1,0,3,2] should NOT fit."""
        shapes, regions = parse_input(self.test_file)
        all_orientations = {i: get_orientations(c) for i, c in shapes.items()}
        w, h, counts = regions[2]
        self.assertFalse(solve_region_backtrack(w, h, counts, all_orientations))

    def test_solve_part1_example(self):
        result = solve_part1(self.test_file)
        self.assertEqual(result, 2)

    def test_area_check_rejects_oversize(self):
        """Region where total piece area exceeds grid area should fail."""
        shapes, _ = parse_input(self.test_file)
        all_orientations = {i: get_orientations(c) for i, c in shapes.items()}
        # 3x3 grid = 9 cells, but 2 shape-4 pieces = 14 cells -> infeasible
        self.assertFalse(solve_region_backtrack(3, 3, [0, 0, 0, 0, 2, 0], all_orientations))

    def test_empty_region(self):
        """Region with no pieces needed should always succeed."""
        shapes, _ = parse_input(self.test_file)
        all_orientations = {i: get_orientations(c) for i, c in shapes.items()}
        self.assertTrue(solve_region_backtrack(4, 4, [0, 0, 0, 0, 0, 0], all_orientations))

    def test_orientations_asymmetric(self):
        """An asymmetric L-shaped piece should have all 8 orientations."""
        l_shape = frozenset({(0, 0), (1, 0), (2, 0), (2, 1)})
        self.assertEqual(len(get_orientations(l_shape)), 8)

    def test_orientations_line(self):
        """A straight line should have 2 orientations (horizontal and vertical)."""
        line = frozenset({(0, 0), (0, 1), (0, 2)})
        self.assertEqual(len(get_orientations(line)), 2)

    def test_normalize(self):
        """Normalize should shift shape so min row and col are 0."""
        cells = frozenset({(3, 5), (4, 5), (4, 6)})
        result = normalize(cells)
        self.assertEqual(result, frozenset({(0, 0), (1, 0), (1, 1)}))

    def test_actual_input_part1(self):
        if os.path.exists("input.txt"):
            result = solve_part1("input.txt")
            print(f"\nPart 1 result: {result}")
            self.assertIsInstance(result, int)
            self.assertEqual(result, 497)


if __name__ == "__main__":
    unittest.main(verbosity=2)
