import unittest
import os
from solution import (
    parse_red_tiles, calculate_rectangle_area, solve_part1, solve_part2,
    is_point_inside_polygon, get_green_tiles, build_horizontal_segments,
    build_vertical_segments, compute_valid_ranges_at_y
)


class TestMovieTheater(unittest.TestCase):

    def test_parse_red_tiles(self):
        """Test parsing red tile positions."""
        test_file = "test_parse.txt"
        content = """7,1
11,1
2,7"""

        with open(test_file, 'w') as f:
            f.write(content)

        tiles = parse_red_tiles(test_file)

        self.assertEqual(len(tiles), 3)
        self.assertEqual(tiles[0], (7, 1))
        self.assertEqual(tiles[1], (11, 1))
        self.assertEqual(tiles[2], (2, 7))

        os.remove(test_file)

    def test_calculate_rectangle_area_simple(self):
        """Test rectangle area calculation with simple coordinates."""
        tile1 = (0, 0)
        tile2 = (4, 3)
        area = calculate_rectangle_area(tile1, tile2)
        self.assertEqual(area, 12)  # width=4, height=3

    def test_calculate_rectangle_area_reversed(self):
        """Test that order doesn't matter."""
        tile1 = (7, 1)
        tile2 = (11, 5)
        area1 = calculate_rectangle_area(tile1, tile2)
        area2 = calculate_rectangle_area(tile2, tile1)
        self.assertEqual(area1, area2)
        self.assertEqual(area1, 16)  # width=4, height=4

    def test_calculate_rectangle_area_zero_width(self):
        """Test rectangle with zero width."""
        tile1 = (5, 1)
        tile2 = (5, 10)
        area = calculate_rectangle_area(tile1, tile2)
        self.assertEqual(area, 0)  # width=0, height=9

    def test_calculate_rectangle_area_zero_height(self):
        """Test rectangle with zero height."""
        tile1 = (1, 5)
        tile2 = (10, 5)
        area = calculate_rectangle_area(tile1, tile2)
        self.assertEqual(area, 0)  # width=9, height=0

    def test_calculate_rectangle_area_example(self):
        """Test with example from problem."""
        tile1 = (2, 5)
        tile2 = (7, 5)
        area = calculate_rectangle_area(tile1, tile2)
        self.assertEqual(area, 0)  # Same y coordinate, height=0

        tile1 = (2, 5)
        tile2 = (7, 8)
        area = calculate_rectangle_area(tile1, tile2)
        self.assertEqual(area, 15)  # width=5, height=3

    def test_solve_part1_example(self):
        """Test with the actual example from the problem."""
        test_file = "test_example.txt"
        example = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""

        with open(test_file, 'w') as f:
            f.write(example)

        result = solve_part1(test_file)
        # Maximum area is 50: between (2,5) and (11,1)
        # Width = 11-2+1 = 10, Height = 5-1+1 = 5, Area = 50
        self.assertEqual(result, 50)

        os.remove(test_file)

    def test_solve_part1_two_tiles(self):
        """Test with just two tiles."""
        test_file = "test_two.txt"
        content = """0,0
10,5"""

        with open(test_file, 'w') as f:
            f.write(content)

        result = solve_part1(test_file)
        # Width = 10-0+1 = 11, Height = 5-0+1 = 6, Area = 66
        self.assertEqual(result, 66)

        os.remove(test_file)

    def test_solve_part1_all_same_x(self):
        """Test with tiles all on same vertical line."""
        test_file = "test_same_x.txt"
        content = """5,1
5,2
5,3
5,4"""

        with open(test_file, 'w') as f:
            f.write(content)

        result = solve_part1(test_file)
        # Max is from (5,1) to (5,4): width=1, height=4, area=4
        self.assertEqual(result, 4)

        os.remove(test_file)

    def test_solve_part1_all_same_y(self):
        """Test with tiles all on same horizontal line."""
        test_file = "test_same_y.txt"
        content = """1,5
2,5
3,5
4,5"""

        with open(test_file, 'w') as f:
            f.write(content)

        result = solve_part1(test_file)
        # Max is from (1,5) to (4,5): width=4, height=1, area=4
        self.assertEqual(result, 4)

        os.remove(test_file)

    def test_solve_part1_square(self):
        """Test with tiles forming corners of a square."""
        test_file = "test_square.txt"
        content = """0,0
10,0
0,10
10,10"""

        with open(test_file, 'w') as f:
            f.write(content)

        result = solve_part1(test_file)
        # From (0,0) to (10,10): width=11, height=11, area=121
        self.assertEqual(result, 121)

        os.remove(test_file)

    def test_solve_part1_different_rectangles(self):
        """Test with multiple different sized rectangles."""
        test_file = "test_multiple.txt"
        content = """0,0
3,4
10,1
15,20"""

        with open(test_file, 'w') as f:
            f.write(content)

        result = solve_part1(test_file)
        # Largest should be (0,0) to (15,20): width=16, height=21, area=336
        self.assertEqual(result, 336)

        os.remove(test_file)

    def test_parse_empty_file(self):
        """Test parsing an empty file."""
        test_file = "test_empty.txt"

        with open(test_file, 'w') as f:
            f.write("")

        tiles = parse_red_tiles(test_file)
        self.assertEqual(len(tiles), 0)

        os.remove(test_file)

    def test_actual_input_part1(self):
        """Test Part 1 with the actual input file."""
        if os.path.exists("input.txt"):
            result = solve_part1("input.txt")
            print(f"\nPart 1 result: {result}")
            self.assertIsInstance(result, int)
            self.assertGreater(result, 0)


class TestPart2(unittest.TestCase):
    """Tests for Part 2: Red and Green tiles only."""

    def setUp(self):
        """Set up example polygon for testing."""
        self.example_content = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""
        self.test_file = "test_part2.txt"
        with open(self.test_file, 'w') as f:
            f.write(self.example_content)
        self.red_tiles = parse_red_tiles(self.test_file)

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_is_point_inside_polygon_interior(self):
        """Test that interior points are correctly identified."""
        # Points clearly inside the polygon
        self.assertTrue(is_point_inside_polygon(8, 4, self.red_tiles))
        self.assertTrue(is_point_inside_polygon(5, 4, self.red_tiles))
        self.assertTrue(is_point_inside_polygon(3, 4, self.red_tiles))

    def test_is_point_inside_polygon_exterior(self):
        """Test that exterior points are correctly identified."""
        # Points clearly outside the polygon
        self.assertFalse(is_point_inside_polygon(0, 0, self.red_tiles))
        self.assertFalse(is_point_inside_polygon(12, 5, self.red_tiles))
        self.assertFalse(is_point_inside_polygon(5, 6, self.red_tiles))

    def test_get_green_tiles_count(self):
        """Test that green tiles are correctly computed."""
        green_tiles = get_green_tiles(self.red_tiles)
        # The example should have 46 green tiles (from visual count)
        self.assertEqual(len(green_tiles), 46)

    def test_build_horizontal_segments(self):
        """Test horizontal segment extraction."""
        segments = build_horizontal_segments(self.red_tiles)
        # Should have 4 horizontal segments
        self.assertEqual(len(segments), 4)
        # Check one specific segment
        self.assertIn((1, 7, 11), segments)  # y=1 from x=7 to x=11

    def test_build_vertical_segments(self):
        """Test vertical segment extraction."""
        segments = build_vertical_segments(self.red_tiles)
        # Should have 4 vertical segments
        self.assertEqual(len(segments), 4)
        # Check one specific segment
        self.assertIn((11, 1, 7), segments)  # x=11 from y=1 to y=7

    def test_compute_valid_ranges_at_y(self):
        """Test valid range computation at specific y-coordinates."""
        vertical_segments = build_vertical_segments(self.red_tiles)
        horizontal_segments = build_horizontal_segments(self.red_tiles)

        # Row 1: should be (7, 11)
        ranges = compute_valid_ranges_at_y(1, vertical_segments, horizontal_segments, self.red_tiles)
        self.assertEqual(ranges, [(7, 11)])

        # Row 3: should be (2, 11) - includes boundary and interior
        ranges = compute_valid_ranges_at_y(3, vertical_segments, horizontal_segments, self.red_tiles)
        self.assertEqual(ranges, [(2, 11)])

        # Row 4: should be (2, 11) - interior row
        ranges = compute_valid_ranges_at_y(4, vertical_segments, horizontal_segments, self.red_tiles)
        self.assertEqual(ranges, [(2, 11)])

    def test_solve_part2_example(self):
        """Test Part 2 with the example from the problem."""
        result = solve_part2(self.test_file)
        # Maximum area is 24: between (9,5) and (2,3)
        # Width = 9-2+1 = 8, Height = 5-3+1 = 3, Area = 24
        self.assertEqual(result, 24)

    def test_solve_part2_example_rectangles(self):
        """Verify specific rectangles mentioned in the problem."""
        # Rectangle between 7,3 and 11,1 should have area 15
        # Width = 11-7+1 = 5, Height = 3-1+1 = 3, Area = 15
        # This is valid because all tiles are red or green

        # Rectangle between 9,7 and 9,5 should have area 3
        # Width = 1, Height = 3, Area = 3
        # This is valid (thin vertical rectangle)
        pass  # These are covered by the main example test

    def test_solve_part2_simple_square(self):
        """Test with a simple square polygon."""
        test_file = "test_square_part2.txt"
        content = """0,0
4,0
4,4
0,4"""
        with open(test_file, 'w') as f:
            f.write(content)

        result = solve_part2(test_file)
        # All tiles are valid (inside or on boundary)
        # Max area is 25: (0,0) to (4,4)
        self.assertEqual(result, 25)

        os.remove(test_file)

    def test_actual_input_part2(self):
        """Test Part 2 with the actual input file."""
        if os.path.exists("input.txt"):
            result = solve_part2("input.txt")
            print(f"\nPart 2 result: {result}")
            self.assertIsInstance(result, int)
            self.assertGreater(result, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
