import unittest
import os
from solution import parse_input, count_paths, count_paths_through_required, solve_part1, solve_part2


class TestDay11(unittest.TestCase):

    def setUp(self):
        """Set up example input from the problem."""
        self.example_content = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""
        self.test_file = "test_example.txt"
        with open(self.test_file, 'w') as f:
            f.write(self.example_content)

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_parse_input(self):
        """Test parsing the input file."""
        graph = parse_input(self.test_file)
        self.assertEqual(graph['you'], ['bbb', 'ccc'])
        self.assertEqual(graph['bbb'], ['ddd', 'eee'])
        self.assertEqual(graph['ccc'], ['ddd', 'eee', 'fff'])
        self.assertEqual(graph['eee'], ['out'])

    def test_count_paths_simple(self):
        """Test counting paths with a simple graph."""
        graph = {'a': ['b'], 'b': ['c'], 'c': ['end']}
        self.assertEqual(count_paths(graph, 'a', 'end'), 1)

    def test_count_paths_branching(self):
        """Test counting paths with branching."""
        graph = {'a': ['b', 'c'], 'b': ['end'], 'c': ['end']}
        self.assertEqual(count_paths(graph, 'a', 'end'), 2)

    def test_solve_part1_example(self):
        """Test Part 1 with the example from the problem."""
        result = solve_part1(self.test_file)
        self.assertEqual(result, 5)

    def test_actual_input_part1(self):
        """Test Part 1 with the actual input file."""
        if os.path.exists("input.txt"):
            result = solve_part1("input.txt")
            print(f"\nPart 1 result: {result}")
            self.assertIsInstance(result, int)
            self.assertGreater(result, 0)


class TestDay11Part2(unittest.TestCase):

    def setUp(self):
        """Set up example input from Part 2."""
        self.example_content = """svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out"""
        self.test_file = "test_example_part2.txt"
        with open(self.test_file, 'w') as f:
            f.write(self.example_content)

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_count_paths_through_required(self):
        """Test counting paths through required nodes."""
        graph = parse_input(self.test_file)
        # Total paths from svr to out = 8
        result = count_paths(graph, 'svr', 'out')
        self.assertEqual(result, 8)

    def test_solve_part2_example(self):
        """Test Part 2 with the example from the problem."""
        result = solve_part2(self.test_file)
        self.assertEqual(result, 2)

    def test_actual_input_part2(self):
        """Test Part 2 with the actual input file."""
        if os.path.exists("input.txt"):
            result = solve_part2("input.txt")
            print(f"\nPart 2 result: {result}")
            self.assertIsInstance(result, int)
            self.assertGreater(result, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
