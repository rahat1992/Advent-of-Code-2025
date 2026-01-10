import unittest
import os
from solution import parse_input, is_fresh, count_fresh_ingredients, solve_part1, merge_ranges, count_total_fresh_ids, solve_part2


class TestCafeteria(unittest.TestCase):

    def test_is_fresh_in_range(self):
        """Test when ingredient ID is within a range."""
        ranges = [(3, 5), (10, 14)]
        self.assertTrue(is_fresh(3, ranges))
        self.assertTrue(is_fresh(4, ranges))
        self.assertTrue(is_fresh(5, ranges))
        self.assertTrue(is_fresh(10, ranges))
        self.assertTrue(is_fresh(14, ranges))

    def test_is_fresh_outside_range(self):
        """Test when ingredient ID is outside all ranges."""
        ranges = [(3, 5), (10, 14)]
        self.assertFalse(is_fresh(1, ranges))
        self.assertFalse(is_fresh(2, ranges))
        self.assertFalse(is_fresh(6, ranges))
        self.assertFalse(is_fresh(9, ranges))
        self.assertFalse(is_fresh(15, ranges))

    def test_is_fresh_overlapping_ranges(self):
        """Test when ranges overlap."""
        ranges = [(3, 5), (10, 14), (16, 20), (12, 18)]
        # 17 is in both (16, 20) and (12, 18)
        self.assertTrue(is_fresh(17, ranges))
        # 12 is in both (10, 14) and (12, 18)
        self.assertTrue(is_fresh(12, ranges))

    def test_is_fresh_single_value_range(self):
        """Test when range has only one value."""
        ranges = [(5, 5), (10, 10)]
        self.assertTrue(is_fresh(5, ranges))
        self.assertTrue(is_fresh(10, ranges))
        self.assertFalse(is_fresh(4, ranges))
        self.assertFalse(is_fresh(6, ranges))

    def test_is_fresh_empty_ranges(self):
        """Test when there are no ranges."""
        ranges = []
        self.assertFalse(is_fresh(5, ranges))
        self.assertFalse(is_fresh(100, ranges))

    def test_count_fresh_ingredients_example(self):
        """Test with the example from the problem."""
        ranges = [(3, 5), (10, 14), (16, 20), (12, 18)]
        ingredient_ids = [1, 5, 8, 11, 17, 32]
        # Fresh: 5, 11, 17 (3 total)
        self.assertEqual(count_fresh_ingredients(ranges, ingredient_ids), 3)

    def test_count_fresh_ingredients_all_fresh(self):
        """Test when all ingredients are fresh."""
        ranges = [(1, 100)]
        ingredient_ids = [5, 10, 50, 100]
        self.assertEqual(count_fresh_ingredients(ranges, ingredient_ids), 4)

    def test_count_fresh_ingredients_none_fresh(self):
        """Test when no ingredients are fresh."""
        ranges = [(1, 5), (10, 15)]
        ingredient_ids = [6, 7, 8, 9, 16, 20]
        self.assertEqual(count_fresh_ingredients(ranges, ingredient_ids), 0)

    def test_count_fresh_ingredients_some_fresh(self):
        """Test with a mix of fresh and spoiled ingredients."""
        ranges = [(1, 5), (10, 15)]
        ingredient_ids = [3, 7, 12, 20]
        # Fresh: 3 (in 1-5), 12 (in 10-15) = 2
        self.assertEqual(count_fresh_ingredients(ranges, ingredient_ids), 2)

    def test_parse_input_example(self):
        """Test parsing the example input."""
        test_file = "test_input.txt"
        example_input = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

        with open(test_file, 'w') as f:
            f.write(example_input)

        ranges, ingredient_ids = parse_input(test_file)

        # Check ranges
        self.assertEqual(ranges, [(3, 5), (10, 14), (16, 20), (12, 18)])

        # Check ingredient IDs
        self.assertEqual(ingredient_ids, [1, 5, 8, 11, 17, 32])

        os.remove(test_file)

    def test_solve_part1_example(self):
        """Test Part 1 with the example from the problem."""
        test_file = "test_input.txt"
        example_input = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

        with open(test_file, 'w') as f:
            f.write(example_input)

        result = solve_part1(test_file)
        self.assertEqual(result, 3)

        os.remove(test_file)

    def test_count_fresh_large_ranges(self):
        """Test with large range values."""
        ranges = [(1000000, 2000000), (5000000, 6000000)]
        ingredient_ids = [1500000, 3000000, 5500000]
        # Fresh: 1500000, 5500000 = 2
        self.assertEqual(count_fresh_ingredients(ranges, ingredient_ids), 2)

    def test_count_fresh_adjacent_ranges(self):
        """Test with adjacent ranges."""
        ranges = [(1, 5), (6, 10)]
        ingredient_ids = [5, 6, 11]
        # Fresh: 5 (in 1-5), 6 (in 6-10) = 2
        self.assertEqual(count_fresh_ingredients(ranges, ingredient_ids), 2)

    def test_count_fresh_overlapping_multiple(self):
        """Test with multiple overlapping ranges."""
        ranges = [(1, 10), (5, 15), (12, 20)]
        ingredient_ids = [3, 7, 13, 25]
        # Fresh: 3 (in 1-10), 7 (in 1-10 and 5-15), 13 (in 5-15 and 12-20) = 3
        self.assertEqual(count_fresh_ingredients(ranges, ingredient_ids), 3)

    def test_is_fresh_boundary_values(self):
        """Test boundary values of ranges."""
        ranges = [(10, 20), (30, 40)]
        # Test exact boundaries
        self.assertTrue(is_fresh(10, ranges))
        self.assertTrue(is_fresh(20, ranges))
        self.assertTrue(is_fresh(30, ranges))
        self.assertTrue(is_fresh(40, ranges))
        # Test just outside boundaries
        self.assertFalse(is_fresh(9, ranges))
        self.assertFalse(is_fresh(21, ranges))
        self.assertFalse(is_fresh(29, ranges))
        self.assertFalse(is_fresh(41, ranges))

    def test_actual_input_part1(self):
        """Test Part 1 with the actual input file."""
        if os.path.exists("input.txt"):
            result = solve_part1("input.txt")
            self.assertEqual(result, 679)

    # Part 2 Tests
    def test_merge_ranges_no_overlap(self):
        """Test merging ranges with no overlap."""
        ranges = [(1, 3), (5, 7), (9, 10)]
        merged = merge_ranges(ranges)
        self.assertEqual(merged, [(1, 3), (5, 7), (9, 10)])

    def test_merge_ranges_complete_overlap(self):
        """Test merging ranges where one is completely inside another."""
        ranges = [(1, 10), (3, 5)]
        merged = merge_ranges(ranges)
        self.assertEqual(merged, [(1, 10)])

    def test_merge_ranges_partial_overlap(self):
        """Test merging ranges with partial overlap."""
        ranges = [(1, 5), (3, 8), (7, 10)]
        merged = merge_ranges(ranges)
        self.assertEqual(merged, [(1, 10)])

    def test_merge_ranges_adjacent(self):
        """Test merging adjacent ranges (should merge)."""
        ranges = [(1, 5), (6, 10)]
        merged = merge_ranges(ranges)
        self.assertEqual(merged, [(1, 10)])

    def test_merge_ranges_almost_adjacent(self):
        """Test ranges that are close but not adjacent."""
        ranges = [(1, 5), (7, 10)]
        merged = merge_ranges(ranges)
        self.assertEqual(merged, [(1, 5), (7, 10)])

    def test_merge_ranges_example(self):
        """Test merging with the example from the problem."""
        ranges = [(3, 5), (10, 14), (16, 20), (12, 18)]
        merged = merge_ranges(ranges)
        # Should merge (10, 14) and (12, 18) to (10, 18), then (16, 20) to (10, 20)
        self.assertEqual(merged, [(3, 5), (10, 20)])

    def test_merge_ranges_unsorted(self):
        """Test that merge_ranges handles unsorted input."""
        ranges = [(10, 15), (1, 5), (3, 7)]
        merged = merge_ranges(ranges)
        self.assertEqual(merged, [(1, 7), (10, 15)])

    def test_merge_ranges_single_range(self):
        """Test merging a single range."""
        ranges = [(5, 10)]
        merged = merge_ranges(ranges)
        self.assertEqual(merged, [(5, 10)])

    def test_merge_ranges_empty(self):
        """Test merging an empty list of ranges."""
        ranges = []
        merged = merge_ranges(ranges)
        self.assertEqual(merged, [])

    def test_merge_ranges_single_value(self):
        """Test ranges with single values."""
        ranges = [(5, 5), (7, 7), (6, 6)]
        merged = merge_ranges(ranges)
        # All adjacent, should merge to (5, 7)
        self.assertEqual(merged, [(5, 7)])

    def test_merge_ranges_multiple_merges(self):
        """Test multiple overlapping ranges that need to be merged."""
        ranges = [(1, 3), (2, 5), (4, 8), (7, 10), (15, 20)]
        merged = merge_ranges(ranges)
        self.assertEqual(merged, [(1, 10), (15, 20)])

    def test_count_total_fresh_ids_simple(self):
        """Test counting total fresh IDs with simple ranges."""
        ranges = [(1, 5), (10, 15)]
        # 1-5 = 5 IDs, 10-15 = 6 IDs, total = 11
        self.assertEqual(count_total_fresh_ids(ranges), 11)

    def test_count_total_fresh_ids_overlapping(self):
        """Test counting with overlapping ranges (should not double-count)."""
        ranges = [(1, 10), (5, 15)]
        # Merged to (1, 15) = 15 IDs
        self.assertEqual(count_total_fresh_ids(ranges), 15)

    def test_count_total_fresh_ids_example(self):
        """Test counting with the example from the problem."""
        ranges = [(3, 5), (10, 14), (16, 20), (12, 18)]
        # 3-5 = 3 IDs, 10-20 = 11 IDs (after merging), total = 14
        self.assertEqual(count_total_fresh_ids(ranges), 14)

    def test_count_total_fresh_ids_single_range(self):
        """Test counting with a single range."""
        ranges = [(100, 200)]
        # 100-200 inclusive = 101 IDs
        self.assertEqual(count_total_fresh_ids(ranges), 101)

    def test_count_total_fresh_ids_single_value(self):
        """Test counting with single-value ranges."""
        ranges = [(5, 5), (10, 10)]
        # Two single IDs = 2 total
        self.assertEqual(count_total_fresh_ids(ranges), 2)

    def test_count_total_fresh_ids_adjacent(self):
        """Test counting with adjacent ranges."""
        ranges = [(1, 5), (6, 10), (11, 15)]
        # All merge to (1, 15) = 15 IDs
        self.assertEqual(count_total_fresh_ids(ranges), 15)

    def test_count_total_fresh_ids_empty(self):
        """Test counting with no ranges."""
        ranges = []
        self.assertEqual(count_total_fresh_ids(ranges), 0)

    def test_count_total_fresh_ids_large_values(self):
        """Test counting with large range values."""
        ranges = [(1000000, 2000000)]
        # 2000000 - 1000000 + 1 = 1000001
        self.assertEqual(count_total_fresh_ids(ranges), 1000001)

    def test_solve_part2_example(self):
        """Test Part 2 with the example from the problem."""
        test_file = "test_input_part2.txt"
        example_input = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""

        with open(test_file, 'w') as f:
            f.write(example_input)

        result = solve_part2(test_file)
        self.assertEqual(result, 14)

        os.remove(test_file)

    def test_actual_input_part2(self):
        """Test Part 2 with the actual input file."""
        if os.path.exists("input.txt"):
            result = solve_part2("input.txt")
            self.assertEqual(result, 358155203664116)


if __name__ == "__main__":
    unittest.main(verbosity=2)
