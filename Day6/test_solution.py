import unittest
import os
from solution import parse_worksheet, parse_worksheet_rtl, solve_problem, solve_part1, solve_part2


class TestCephalopodMath(unittest.TestCase):

    def test_solve_problem_multiply(self):
        """Test solving a multiplication problem."""
        numbers = [123, 45, 6]
        operation = '*'
        # 123 * 45 * 6 = 33210
        self.assertEqual(solve_problem(numbers, operation), 33210)

    def test_solve_problem_add(self):
        """Test solving an addition problem."""
        numbers = [328, 64, 98]
        operation = '+'
        # 328 + 64 + 98 = 490
        self.assertEqual(solve_problem(numbers, operation), 490)

    def test_solve_problem_single_number(self):
        """Test with a single number."""
        self.assertEqual(solve_problem([42], '*'), 42)
        self.assertEqual(solve_problem([42], '+'), 42)

    def test_solve_problem_two_numbers_multiply(self):
        """Test multiplication with two numbers."""
        self.assertEqual(solve_problem([7, 8], '*'), 56)

    def test_solve_problem_two_numbers_add(self):
        """Test addition with two numbers."""
        self.assertEqual(solve_problem([7, 8], '+'), 15)

    def test_solve_problem_empty_list(self):
        """Test with empty list."""
        self.assertEqual(solve_problem([], '*'), 0)
        self.assertEqual(solve_problem([], '+'), 0)

    def test_solve_problem_large_multiplication(self):
        """Test with larger numbers in multiplication."""
        numbers = [51, 387, 215]
        operation = '*'
        # 51 * 387 * 215 = 4243455
        self.assertEqual(solve_problem(numbers, operation), 4243455)

    def test_solve_problem_many_numbers_add(self):
        """Test addition with many numbers."""
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        operation = '+'
        # Sum of 1-10 = 55
        self.assertEqual(solve_problem(numbers, operation), 55)

    def test_solve_problem_many_numbers_multiply(self):
        """Test multiplication with many numbers."""
        numbers = [2, 3, 4]
        operation = '*'
        # 2 * 3 * 4 = 24
        self.assertEqual(solve_problem(numbers, operation), 24)

    def test_parse_worksheet_example(self):
        """Test parsing the example from the problem."""
        test_file = "test_input.txt"
        example_input = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  """

        with open(test_file, 'w') as f:
            f.write(example_input)

        problems = parse_worksheet(test_file)

        # Should have 4 problems
        self.assertEqual(len(problems), 4)

        # Check each problem
        # Problem 1: 123, 45, 6 with *
        self.assertEqual(problems[0][0], [123, 45, 6])
        self.assertEqual(problems[0][1], '*')

        # Problem 2: 328, 64, 98 with +
        self.assertEqual(problems[1][0], [328, 64, 98])
        self.assertEqual(problems[1][1], '+')

        # Problem 3: 51, 387, 215 with *
        self.assertEqual(problems[2][0], [51, 387, 215])
        self.assertEqual(problems[2][1], '*')

        # Problem 4: 64, 23, 314 with +
        self.assertEqual(problems[3][0], [64, 23, 314])
        self.assertEqual(problems[3][1], '+')

        os.remove(test_file)

    def test_parse_worksheet_single_problem(self):
        """Test parsing a worksheet with a single problem."""
        test_file = "test_single.txt"
        example_input = """10
20
30
+"""

        with open(test_file, 'w') as f:
            f.write(example_input)

        problems = parse_worksheet(test_file)

        self.assertEqual(len(problems), 1)
        self.assertEqual(problems[0][0], [10, 20, 30])
        self.assertEqual(problems[0][1], '+')

        os.remove(test_file)

    def test_parse_worksheet_two_problems_far_apart(self):
        """Test parsing problems with lots of space between them."""
        test_file = "test_spaced.txt"
        example_input = """10      50
20      60
+       *"""

        with open(test_file, 'w') as f:
            f.write(example_input)

        problems = parse_worksheet(test_file)

        self.assertEqual(len(problems), 2)
        self.assertEqual(problems[0][0], [10, 20])
        self.assertEqual(problems[0][1], '+')
        self.assertEqual(problems[1][0], [50, 60])
        self.assertEqual(problems[1][1], '*')

        os.remove(test_file)

    def test_parse_worksheet_different_row_counts(self):
        """Test problems with different numbers of rows."""
        test_file = "test_diff_rows.txt"
        example_input = """10 5
   6
   7
+  *"""

        with open(test_file, 'w') as f:
            f.write(example_input)

        problems = parse_worksheet(test_file)

        self.assertEqual(len(problems), 2)
        self.assertEqual(problems[0][0], [10])
        self.assertEqual(problems[0][1], '+')
        self.assertEqual(problems[1][0], [5, 6, 7])
        self.assertEqual(problems[1][1], '*')

        os.remove(test_file)

    def test_solve_part1_example(self):
        """Test Part 1 with the example from the problem."""
        test_file = "test_part1.txt"
        example_input = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +  """

        with open(test_file, 'w') as f:
            f.write(example_input)

        result = solve_part1(test_file)
        # 33210 + 490 + 4243455 + 401 = 4277556
        self.assertEqual(result, 4277556)

        os.remove(test_file)

    def test_solve_part1_all_addition(self):
        """Test with all addition problems."""
        test_file = "test_all_add.txt"
        example_input = """10 20
10 20
+  +"""

        with open(test_file, 'w') as f:
            f.write(example_input)

        result = solve_part1(test_file)
        # (10 + 10) + (20 + 20) = 20 + 40 = 60
        self.assertEqual(result, 60)

        os.remove(test_file)

    def test_solve_part1_all_multiplication(self):
        """Test with all multiplication problems."""
        test_file = "test_all_mult.txt"
        example_input = """2 3
2 3
*  *"""

        with open(test_file, 'w') as f:
            f.write(example_input)

        result = solve_part1(test_file)
        # (2 * 2) + (3 * 3) = 4 + 9 = 13
        self.assertEqual(result, 13)

        os.remove(test_file)

    def test_solve_part1_single_problem(self):
        """Test with a single problem."""
        test_file = "test_single_prob.txt"
        example_input = """5
10
15
+"""

        with open(test_file, 'w') as f:
            f.write(example_input)

        result = solve_part1(test_file)
        # 5 + 10 + 15 = 30
        self.assertEqual(result, 30)

        os.remove(test_file)

    def test_solve_part1_large_numbers(self):
        """Test with large numbers."""
        test_file = "test_large.txt"
        example_input = """1000 2000
1000 2000
*    +"""

        with open(test_file, 'w') as f:
            f.write(example_input)

        result = solve_part1(test_file)
        # (1000 * 1000) + (2000 + 2000) = 1000000 + 4000 = 1004000
        self.assertEqual(result, 1004000)

        os.remove(test_file)

    def test_actual_input_part1(self):
        """Test Part 1 with the actual input file."""
        if os.path.exists("input.txt"):
            result = solve_part1("input.txt")
            self.assertEqual(result, 5784380717354)

    def test_parse_worksheet_right_aligned_numbers(self):
        """Test parsing with right-aligned numbers."""
        test_file = "test_align.txt"
        example_input = """ 100   50
  20    5
   1
 +     *"""

        with open(test_file, 'w') as f:
            f.write(example_input)

        problems = parse_worksheet(test_file)

        # This should parse as 2 problems
        self.assertEqual(len(problems), 2)
        self.assertEqual(problems[0][0], [100, 20, 1])
        self.assertEqual(problems[0][1], '+')
        self.assertEqual(problems[1][0], [50, 5])
        self.assertEqual(problems[1][1], '*')

        os.remove(test_file)

    def test_solve_problem_zero_in_multiplication(self):
        """Test multiplication with zero."""
        numbers = [5, 0, 10]
        operation = '*'
        self.assertEqual(solve_problem(numbers, operation), 0)

    def test_solve_problem_zero_in_addition(self):
        """Test addition with zeros."""
        numbers = [0, 5, 0, 10]
        operation = '+'
        self.assertEqual(solve_problem(numbers, operation), 15)

    def test_solve_problem_all_ones_multiply(self):
        """Test multiplying all ones."""
        numbers = [1, 1, 1, 1, 1]
        operation = '*'
        self.assertEqual(solve_problem(numbers, operation), 1)

    def test_solve_problem_all_ones_add(self):
        """Test adding all ones."""
        numbers = [1, 1, 1, 1, 1]
        operation = '+'
        self.assertEqual(solve_problem(numbers, operation), 5)

    # Part 2 Tests
    def test_parse_worksheet_rtl_example(self):
        """Test parsing the example from Part 2."""
        test_file = "test_rtl.txt"
        example_input = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +"""

        with open(test_file, 'w') as f:
            f.write(example_input)

        problems = parse_worksheet_rtl(test_file)

        # Should have 4 problems
        self.assertEqual(len(problems), 4)

        # Check each problem (reading right-to-left)
        # Problem 1 (leftmost): 356 * 24 * 1
        self.assertEqual(problems[0][0], [356, 24, 1])
        self.assertEqual(problems[0][1], '*')

        # Problem 2: 8 + 248 + 369
        self.assertEqual(problems[1][0], [8, 248, 369])
        self.assertEqual(problems[1][1], '+')

        # Problem 3: 175 * 581 * 32
        self.assertEqual(problems[2][0], [175, 581, 32])
        self.assertEqual(problems[2][1], '*')

        # Problem 4 (rightmost): 4 + 431 + 623
        self.assertEqual(problems[3][0], [4, 431, 623])
        self.assertEqual(problems[3][1], '+')

        os.remove(test_file)

    def test_parse_worksheet_rtl_single_column_numbers(self):
        """Test parsing RTL with single-digit numbers."""
        test_file = "test_rtl_single.txt"
        example_input = """1 2
3 4
+ *"""

        with open(test_file, 'w') as f:
            f.write(example_input)

        problems = parse_worksheet_rtl(test_file)

        self.assertEqual(len(problems), 2)
        # First problem (leftmost): 13 +
        self.assertEqual(problems[0][0], [13])
        self.assertEqual(problems[0][1], '+')
        # Second problem (rightmost): 24 *
        self.assertEqual(problems[1][0], [24])
        self.assertEqual(problems[1][1], '*')

        os.remove(test_file)

    def test_parse_worksheet_rtl_multi_digit_columns(self):
        """Test parsing RTL where each column has multiple digits."""
        test_file = "test_rtl_multi.txt"
        example_input = """12 34
56 78
+  *"""

        with open(test_file, 'w') as f:
            f.write(example_input)

        problems = parse_worksheet_rtl(test_file)

        self.assertEqual(len(problems), 2)
        # First problem (leftmost): read cols 1 then 0: 26 + 15
        self.assertEqual(problems[0][0], [26, 15])
        self.assertEqual(problems[0][1], '+')
        # Second problem (rightmost): read cols 4 then 3: 48 * 37
        self.assertEqual(problems[1][0], [48, 37])
        self.assertEqual(problems[1][1], '*')

        os.remove(test_file)

    def test_solve_part2_example(self):
        """Test Part 2 with the example from the problem."""
        test_file = "test_part2.txt"
        example_input = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +"""

        with open(test_file, 'w') as f:
            f.write(example_input)

        result = solve_part2(test_file)
        # 8544 + 625 + 3253600 + 1058 = 3263827
        self.assertEqual(result, 3263827)

        os.remove(test_file)

    def test_parse_worksheet_rtl_different_heights(self):
        """Test parsing RTL where columns have different heights."""
        test_file = "test_rtl_heights.txt"
        example_input = """1   5
2   6
3   7
    8
+   *"""

        with open(test_file, 'w') as f:
            f.write(example_input)

        problems = parse_worksheet_rtl(test_file)

        self.assertEqual(len(problems), 2)
        # First problem (leftmost): single column with 123
        self.assertEqual(problems[0][0], [123])
        self.assertEqual(problems[0][1], '+')
        # Second problem (rightmost): single column with 5678
        self.assertEqual(problems[1][0], [5678])
        self.assertEqual(problems[1][1], '*')

        os.remove(test_file)

    def test_solve_part2_simple_addition(self):
        """Test Part 2 with simple addition."""
        test_file = "test_part2_add.txt"
        example_input = """1 2
2 3
+ +"""

        with open(test_file, 'w') as f:
            f.write(example_input)

        result = solve_part2(test_file)
        # First (leftmost): 12, Second (rightmost): 23, Total: 12 + 23 = 35
        self.assertEqual(result, 35)

        os.remove(test_file)

    def test_solve_part2_simple_multiplication(self):
        """Test Part 2 with simple multiplication."""
        test_file = "test_part2_mult.txt"
        example_input = """2 3
3 4
* *"""

        with open(test_file, 'w') as f:
            f.write(example_input)

        result = solve_part2(test_file)
        # First (leftmost): 23, Second (rightmost): 34, Total: 23 + 34 = 57
        self.assertEqual(result, 57)

        os.remove(test_file)

    def test_actual_input_part2(self):
        """Test Part 2 with the actual input file."""
        if os.path.exists("input.txt"):
            result = solve_part2("input.txt")
            self.assertEqual(result, 7996218225744)


if __name__ == "__main__":
    unittest.main(verbosity=2)
