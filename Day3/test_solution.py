import unittest
import os
from solution import find_max_joltage, find_max_joltage_n_batteries, solve_part1, solve_part2


class TestLobby(unittest.TestCase):

    def test_find_max_joltage_example1(self):
        """Test example 1: 987654321111111 should give 98"""
        self.assertEqual(find_max_joltage("987654321111111"), 98)

    def test_find_max_joltage_example2(self):
        """Test example 2: 811111111111119 should give 89"""
        self.assertEqual(find_max_joltage("811111111111119"), 89)

    def test_find_max_joltage_example3(self):
        """Test example 3: 234234234234278 should give 78"""
        self.assertEqual(find_max_joltage("234234234234278"), 78)

    def test_find_max_joltage_example4(self):
        """Test example 4: 818181911112111 should give 92"""
        self.assertEqual(find_max_joltage("818181911112111"), 92)

    def test_find_max_joltage_simple_cases(self):
        """Test simple cases with obvious maximums."""
        self.assertEqual(find_max_joltage("19"), 19)
        self.assertEqual(find_max_joltage("91"), 91)
        self.assertEqual(find_max_joltage("123"), 23)
        self.assertEqual(find_max_joltage("321"), 32)

    def test_find_max_joltage_all_same(self):
        """Test when all batteries have the same joltage."""
        self.assertEqual(find_max_joltage("1111"), 11)
        self.assertEqual(find_max_joltage("9999"), 99)
        self.assertEqual(find_max_joltage("55555"), 55)

    def test_find_max_joltage_two_batteries(self):
        """Test with exactly two batteries."""
        self.assertEqual(find_max_joltage("12"), 12)
        self.assertEqual(find_max_joltage("99"), 99)
        self.assertEqual(find_max_joltage("45"), 45)

    def test_find_max_joltage_ascending(self):
        """Test with ascending digits."""
        self.assertEqual(find_max_joltage("123456789"), 89)

    def test_find_max_joltage_descending(self):
        """Test with descending digits."""
        self.assertEqual(find_max_joltage("987654321"), 98)

    def test_find_max_joltage_nine_at_end(self):
        """Test when 9 is at the end."""
        self.assertEqual(find_max_joltage("12349"), 49)
        self.assertEqual(find_max_joltage("11119"), 19)

    def test_find_max_joltage_nine_at_start(self):
        """Test when 9 is at the start."""
        self.assertEqual(find_max_joltage("91234"), 94)  # 9 and 4 make 94
        self.assertEqual(find_max_joltage("98765"), 98)  # 9 and 8 make 98

    def test_find_max_joltage_multiple_nines(self):
        """Test with multiple 9s."""
        self.assertEqual(find_max_joltage("9999"), 99)
        self.assertEqual(find_max_joltage("19191"), 99)
        self.assertEqual(find_max_joltage("91919"), 99)

    def test_example_input(self):
        """Test with the example from the problem."""
        test_file = "test_input.txt"
        example_input = """987654321111111
811111111111119
234234234234278
818181911112111"""

        with open(test_file, 'w') as f:
            f.write(example_input)

        result, joltages = solve_part1(test_file)

        # Check individual bank maximums
        self.assertEqual(joltages[0], 98)
        self.assertEqual(joltages[1], 89)
        self.assertEqual(joltages[2], 78)
        self.assertEqual(joltages[3], 92)

        # Check total
        self.assertEqual(result, 357)

        os.remove(test_file)

    def test_actual_input(self):
        """Test with the actual input file."""
        if os.path.exists("input.txt"):
            result, joltages = solve_part1("input.txt")
            self.assertEqual(result, 17554)
            self.assertEqual(len(joltages), 200)

    def test_edge_case_low_digits(self):
        """Test with all low digits."""
        self.assertEqual(find_max_joltage("111111"), 11)
        self.assertEqual(find_max_joltage("222222"), 22)
        self.assertEqual(find_max_joltage("123123"), 33)

    def test_edge_case_mixed(self):
        """Test with mixed high and low digits."""
        self.assertEqual(find_max_joltage("1234567899"), 99)
        self.assertEqual(find_max_joltage("9123456789"), 99)
        self.assertEqual(find_max_joltage("1239456789"), 99)

    # Part 2 Tests
    def test_find_max_joltage_n_batteries_near_full_length(self):
        """Test cases where n is close to or equal to len(bank)."""
        # n == len(bank): should return the full number unchanged
        self.assertEqual(find_max_joltage_n_batteries("123456", 6), 123456)
        self.assertEqual(find_max_joltage_n_batteries("987654321", 9), 987654321)
        # n == len(bank) - 1: should drop a single smallest digit while preserving order
        self.assertEqual(find_max_joltage_n_batteries("123456789", 8), 23456789)
        self.assertEqual(find_max_joltage_n_batteries("987654321", 8), 98765432)

    def test_find_max_joltage_12_batteries_example1(self):
        """Test Part 2 example 1: 987654321111111 should give 987654321111"""
        self.assertEqual(find_max_joltage_n_batteries("987654321111111", 12), 987654321111)

    def test_find_max_joltage_12_batteries_example2(self):
        """Test Part 2 example 2: 811111111111119 should give 811111111119"""
        self.assertEqual(find_max_joltage_n_batteries("811111111111119", 12), 811111111119)

    def test_find_max_joltage_12_batteries_example3(self):
        """Test Part 2 example 3: 234234234234278 should give 434234234278"""
        self.assertEqual(find_max_joltage_n_batteries("234234234234278", 12), 434234234278)

    def test_find_max_joltage_12_batteries_example4(self):
        """Test Part 2 example 4: 818181911112111 should give 888911112111"""
        self.assertEqual(find_max_joltage_n_batteries("818181911112111", 12), 888911112111)

    def test_find_max_joltage_n_batteries_simple(self):
        """Test with simple cases for n batteries."""
        self.assertEqual(find_max_joltage_n_batteries("123456789", 3), 789)
        self.assertEqual(find_max_joltage_n_batteries("987654321", 3), 987)
        self.assertEqual(find_max_joltage_n_batteries("12345", 2), 45)

    def test_find_max_joltage_n_batteries_all_same(self):
        """Test when all batteries have the same joltage."""
        self.assertEqual(find_max_joltage_n_batteries("1111111", 5), 11111)
        self.assertEqual(find_max_joltage_n_batteries("9999999", 5), 99999)

    def test_example_input_part2(self):
        """Test Part 2 with the example from the problem."""
        test_file = "test_input_part2.txt"
        example_input = """987654321111111
811111111111119
234234234234278
818181911112111"""

        with open(test_file, 'w') as f:
            f.write(example_input)

        result, joltages = solve_part2(test_file)

        # Check individual bank maximums
        self.assertEqual(joltages[0], 987654321111)
        self.assertEqual(joltages[1], 811111111119)
        self.assertEqual(joltages[2], 434234234278)
        self.assertEqual(joltages[3], 888911112111)

        # Check total
        self.assertEqual(result, 3121910778619)

        os.remove(test_file)

    def test_actual_input_part2(self):
        """Test Part 2 with the actual input file."""
        if os.path.exists("input.txt"):
            result, joltages = solve_part2("input.txt")
            self.assertEqual(result, 175053592950232)
            self.assertEqual(len(joltages), 200)


if __name__ == "__main__":
    unittest.main(verbosity=2)
