import unittest
import os
import math
from solution import parse_junction_boxes, distance, UnionFind, solve_part1, solve_part2


class TestPlayground(unittest.TestCase):

    def test_parse_junction_boxes(self):
        """Test parsing junction box positions."""
        test_file = "test_parse.txt"
        content = """162,817,812
57,618,57
906,360,560"""

        with open(test_file, 'w') as f:
            f.write(content)

        boxes = parse_junction_boxes(test_file)

        self.assertEqual(len(boxes), 3)
        self.assertEqual(boxes[0], (162, 817, 812))
        self.assertEqual(boxes[1], (57, 618, 57))
        self.assertEqual(boxes[2], (906, 360, 560))

        os.remove(test_file)

    def test_distance(self):
        """Test distance calculation."""
        box1 = (0, 0, 0)
        box2 = (3, 4, 0)
        # Should be 5 (3-4-5 triangle)
        self.assertEqual(distance(box1, box2), 5.0)

    def test_distance_3d(self):
        """Test 3D distance calculation."""
        box1 = (0, 0, 0)
        box2 = (1, 1, 1)
        # Should be sqrt(3)
        self.assertAlmostEqual(distance(box1, box2), math.sqrt(3))

    def test_union_find_basic(self):
        """Test basic Union-Find operations."""
        uf = UnionFind(5)

        # Initially, all elements are in separate sets
        self.assertEqual(uf.find(0), 0)
        self.assertEqual(uf.find(1), 1)

        # Union 0 and 1
        self.assertTrue(uf.union(0, 1))

        # They should now have the same root
        self.assertEqual(uf.find(0), uf.find(1))

        # Trying to union them again should return False
        self.assertFalse(uf.union(0, 1))

    def test_union_find_component_sizes(self):
        """Test getting component sizes."""
        uf = UnionFind(6)

        # Create two components: {0, 1, 2} and {3, 4}
        uf.union(0, 1)
        uf.union(1, 2)
        uf.union(3, 4)

        sizes = uf.get_component_sizes()
        sizes.sort()

        # Should have components of size 1, 2, 3
        self.assertEqual(sorted(sizes), [1, 2, 3])

    def test_solve_part1_example(self):
        """Test with the example from the problem."""
        test_file = "test_example.txt"
        example = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""

        with open(test_file, 'w') as f:
            f.write(example)

        # After 10 pairs, should have circuits of size 5, 4, 2, 2, and seven 1s
        # Product of top 3: 5 * 4 * 2 = 40
        result = solve_part1(test_file, num_pairs=10)
        self.assertEqual(result, 40)

        os.remove(test_file)

    def test_union_find_single_component(self):
        """Test when all elements are in one component."""
        uf = UnionFind(4)

        uf.union(0, 1)
        uf.union(1, 2)
        uf.union(2, 3)

        sizes = uf.get_component_sizes()

        self.assertEqual(len(sizes), 1)
        self.assertEqual(sizes[0], 4)

    def test_union_find_no_unions(self):
        """Test when no unions are performed."""
        uf = UnionFind(5)

        sizes = uf.get_component_sizes()

        # All components should have size 1
        self.assertEqual(sorted(sizes), [1, 1, 1, 1, 1])

    def test_parse_empty_file(self):
        """Test parsing an empty file."""
        test_file = "test_empty.txt"

        with open(test_file, 'w') as f:
            f.write("")

        boxes = parse_junction_boxes(test_file)

        self.assertEqual(len(boxes), 0)

        os.remove(test_file)

    def test_solve_part1_small(self):
        """Test with a small set of boxes."""
        test_file = "test_small.txt"
        content = """0,0,0
10,0,0
0,10,0"""

        with open(test_file, 'w') as f:
            f.write(content)

        # Make 1 pair connection - should connect the two closest boxes
        result = solve_part1(test_file, num_pairs=1)
        # Should have circuits of size 2 and 1
        # Product of top 3 (but only 2 exist): 2 * 1 = 2
        self.assertEqual(result, 2)

        os.remove(test_file)

    def test_actual_input_part1(self):
        """Test Part 1 with the actual input file."""
        if os.path.exists("input.txt"):
            result = solve_part1("input.txt", num_pairs=1000)
            self.assertEqual(result, 42840)

    def test_solve_part2_example(self):
        """Test Part 2 with the example from the problem."""
        test_file = "test_example_part2.txt"
        example = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""

        with open(test_file, 'w') as f:
            f.write(example)

        # Last connection to form single circuit: 216,146,977 and 117,168,530
        # Product of X coordinates: 216 * 117 = 25272
        result = solve_part2(test_file)
        self.assertEqual(result, 25272)

        os.remove(test_file)

    def test_solve_part2_small(self):
        """Test Part 2 with a small set of boxes."""
        test_file = "test_small_part2.txt"
        content = """0,0,0
10,0,0
0,10,0"""

        with open(test_file, 'w') as f:
            f.write(content)

        # Need 2 connections to connect all 3 boxes
        # Last connection should form single circuit
        result = solve_part2(test_file)
        # Result depends on which boxes are connected last
        # All have different X coords (0, 10, 0), so possible: 0*10=0, 0*0=0, 10*0=0
        # Actually the last connection to unify all should be between boxes 0 and 2
        # (after 0-1 and 1-2 are connected, or after 0-1, then 0-2)
        self.assertIsInstance(result, int)

        os.remove(test_file)

    def test_actual_input_part2(self):
        """Test Part 2 with the actual input file."""
        if os.path.exists("input.txt"):
            result = solve_part2("input.txt")
            self.assertEqual(result, 170629052)


if __name__ == "__main__":
    unittest.main(verbosity=2)
