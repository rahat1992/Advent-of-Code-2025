import unittest
import os
from solution import is_invalid_id_part1, is_invalid_id_part2, solve_part1, solve_part2


class TestGiftShop(unittest.TestCase):

    # Part 1 Tests
    def test_is_invalid_id_part1_simple_cases(self):
        """Test simple invalid IDs from the problem for Part 1."""
        # Examples from the problem
        self.assertTrue(is_invalid_id_part1(55))      # 5 twice
        self.assertTrue(is_invalid_id_part1(6464))    # 64 twice
        self.assertTrue(is_invalid_id_part1(123123))  # 123 twice

    def test_is_invalid_id_part1_valid_cases(self):
        """Test valid IDs that should NOT be flagged in Part 1."""
        self.assertFalse(is_invalid_id_part1(101))    # Not a pattern repeated twice
        self.assertFalse(is_invalid_id_part1(123))    # Odd length
        self.assertFalse(is_invalid_id_part1(1234))   # 12 != 34
        self.assertFalse(is_invalid_id_part1(100))    # Odd length

    def test_is_invalid_id_part1_leading_zeros(self):
        """Test that numbers with leading zeros are not considered in Part 1."""
        # 0101 shouldn't be an ID at all - but we're checking numeric values
        # so this would be 101 which is valid
        self.assertFalse(is_invalid_id_part1(101))

    def test_is_invalid_id_part1_from_example_ranges(self):
        """Test specific invalid IDs mentioned in the example for Part 1."""
        self.assertTrue(is_invalid_id_part1(11))          # from 11-22
        self.assertTrue(is_invalid_id_part1(22))          # from 11-22
        self.assertTrue(is_invalid_id_part1(99))          # from 95-115
        self.assertTrue(is_invalid_id_part1(1010))        # from 998-1012
        self.assertTrue(is_invalid_id_part1(1188511885))  # from 1188511880-1188511890
        self.assertTrue(is_invalid_id_part1(222222))      # from 222220-222224
        self.assertTrue(is_invalid_id_part1(446446))      # from 446443-446449
        self.assertTrue(is_invalid_id_part1(38593859))    # from 38593856-38593862

    # Part 2 Tests
    def test_is_invalid_id_part2_examples(self):
        """Test Part 2 examples from the problem."""
        self.assertTrue(is_invalid_id_part2(12341234))    # 1234 two times
        self.assertTrue(is_invalid_id_part2(123123123))   # 123 three times
        self.assertTrue(is_invalid_id_part2(1212121212))  # 12 five times
        self.assertTrue(is_invalid_id_part2(1111111))     # 1 seven times

    def test_is_invalid_id_part2_also_matches_part1(self):
        """Test that Part 2 includes all Part 1 matches."""
        # All Part 1 matches should also be Part 2 matches
        self.assertTrue(is_invalid_id_part2(55))
        self.assertTrue(is_invalid_id_part2(6464))
        self.assertTrue(is_invalid_id_part2(123123))

    def test_is_invalid_id_part2_new_matches(self):
        """Test new matches in Part 2 that weren't in Part 1."""
        self.assertTrue(is_invalid_id_part2(111))      # 1 three times
        self.assertTrue(is_invalid_id_part2(999))      # 9 three times
        self.assertTrue(is_invalid_id_part2(565656))   # 56 three times
        self.assertTrue(is_invalid_id_part2(824824824))     # 824 three times
        self.assertTrue(is_invalid_id_part2(2121212121))    # 21 five times

    def test_range_11_to_22_part1(self):
        """Test the range 11-22 has exactly 11 and 22 as invalid (Part 1)."""
        invalid_in_range = [num for num in range(11, 23) if is_invalid_id_part1(num)]
        self.assertEqual(invalid_in_range, [11, 22])

    def test_range_95_to_115_part1(self):
        """Test the range 95-115 has exactly 99 as invalid (Part 1)."""
        invalid_in_range = [num for num in range(95, 116) if is_invalid_id_part1(num)]
        self.assertEqual(invalid_in_range, [99])

    def test_range_95_to_115_part2(self):
        """Test the range 95-115 has 99 and 111 as invalid (Part 2)."""
        invalid_in_range = [num for num in range(95, 116) if is_invalid_id_part2(num)]
        self.assertEqual(invalid_in_range, [99, 111])

    def test_range_998_to_1012_part1(self):
        """Test the range 998-1012 has exactly 1010 as invalid (Part 1)."""
        invalid_in_range = [num for num in range(998, 1013) if is_invalid_id_part1(num)]
        self.assertEqual(invalid_in_range, [1010])

    def test_range_998_to_1012_part2(self):
        """Test the range 998-1012 has 999 and 1010 as invalid (Part 2)."""
        invalid_in_range = [num for num in range(998, 1013) if is_invalid_id_part2(num)]
        self.assertEqual(invalid_in_range, [999, 1010])

    def test_range_1698522_to_1698528(self):
        """Test the range 1698522-1698528 contains no invalid IDs."""
        invalid_in_range_part1 = [num for num in range(1698522, 1698529) if is_invalid_id_part1(num)]
        self.assertEqual(invalid_in_range_part1, [])
        invalid_in_range_part2 = [num for num in range(1698522, 1698529) if is_invalid_id_part2(num)]
        self.assertEqual(invalid_in_range_part2, [])

    def test_example_input_part1(self):
        """Test Part 1 with the example from the problem."""
        # Create test file with the example
        test_file = "test_input.txt"
        example_input = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124"""

        with open(test_file, 'w') as f:
            f.write(example_input)

        result, invalid_ids = solve_part1(test_file)

        # Expected invalid IDs from the example
        expected_invalid = [11, 22, 99, 1010, 1188511885, 222222, 446446, 38593859]

        # Check that all expected IDs are found
        for expected in expected_invalid:
            self.assertIn(expected, invalid_ids)

        # The example states the sum should be 1227775554
        self.assertEqual(result, 1227775554)

        os.remove(test_file)

    def test_example_input_part2(self):
        """Test Part 2 with the example from the problem."""
        # Create test file with the example
        test_file = "test_input.txt"
        example_input = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124"""

        with open(test_file, 'w') as f:
            f.write(example_input)

        result, invalid_ids = solve_part2(test_file)

        # Expected invalid IDs from the example (Part 2 adds more)
        expected_invalid = [11, 22, 99, 111, 999, 1010, 1188511885, 222222,
                           446446, 38593859, 565656, 824824824, 2121212121]

        # Check that all expected IDs are found
        for expected in expected_invalid:
            self.assertIn(expected, invalid_ids, f"{expected} should be in invalid_ids")

        # The example states the sum should be 4174379265
        self.assertEqual(result, 4174379265)

        os.remove(test_file)

    def test_four_digit_patterns_part1(self):
        """Test various 4-digit patterns for Part 1."""
        self.assertTrue(is_invalid_id_part1(1010))
        self.assertTrue(is_invalid_id_part1(2020))
        self.assertTrue(is_invalid_id_part1(3030))
        self.assertTrue(is_invalid_id_part1(9999))   # 9999 is 99 repeated twice - valid for Part 1
        self.assertFalse(is_invalid_id_part1(1020))
        self.assertFalse(is_invalid_id_part1(1234))

    def test_four_digit_patterns_part2(self):
        """Test various 4-digit patterns for Part 2."""
        self.assertTrue(is_invalid_id_part2(1010))  # 10 twice
        self.assertTrue(is_invalid_id_part2(9999))  # 9 four times
        self.assertTrue(is_invalid_id_part2(1111))  # 1 four times

    def test_six_digit_patterns_part1(self):
        """Test various 6-digit patterns for Part 1."""
        self.assertTrue(is_invalid_id_part1(123123))
        self.assertTrue(is_invalid_id_part1(456456))
        self.assertTrue(is_invalid_id_part1(999999))   # This is 999 repeated twice - valid for Part 1
        self.assertFalse(is_invalid_id_part1(123456))
        self.assertFalse(is_invalid_id_part1(111222))

    def test_six_digit_patterns_part2(self):
        """Test various 6-digit patterns for Part 2."""
        self.assertTrue(is_invalid_id_part2(123123))  # 123 twice
        self.assertTrue(is_invalid_id_part2(999999))  # 9 six times or 99 three times
        self.assertTrue(is_invalid_id_part2(565656))  # 56 three times

    def test_single_digit_repeated_part1(self):
        """Test single digits repeated twice for Part 1."""
        for digit in range(1, 10):  # 1-9 (not 0 due to leading zero rule)
            num_str = str(digit) * 2
            self.assertTrue(is_invalid_id_part1(int(num_str)))

    def test_single_digit_repeated_part2(self):
        """Test single digits repeated multiple times for Part 2."""
        for digit in range(1, 10):
            # Two times
            self.assertTrue(is_invalid_id_part2(int(str(digit) * 2)))
            # Three times
            self.assertTrue(is_invalid_id_part2(int(str(digit) * 3)))
            # Four times
            self.assertTrue(is_invalid_id_part2(int(str(digit) * 4)))

    def test_odd_length_numbers_part1(self):
        """Test that odd-length numbers are never invalid in Part 1."""
        self.assertFalse(is_invalid_id_part1(1))
        self.assertFalse(is_invalid_id_part1(123))
        self.assertFalse(is_invalid_id_part1(12345))
        self.assertFalse(is_invalid_id_part1(1234567))

    def test_odd_length_numbers_part2(self):
        """Test odd-length numbers in Part 2 (some can be invalid)."""
        self.assertFalse(is_invalid_id_part2(1))     # Too short
        self.assertTrue(is_invalid_id_part2(111))    # 1 three times
        self.assertTrue(is_invalid_id_part2(999))    # 9 three times
        self.assertFalse(is_invalid_id_part2(123))   # Not a pattern

    def test_actual_input_part1(self):
        """Test Part 1 with the actual input file."""
        if os.path.exists("input.txt"):
            result, invalid_ids = solve_part1("input.txt")
            self.assertEqual(result, 12850231731)
            self.assertEqual(len(invalid_ids), 807)

    def test_actual_input_part2(self):
        """Test Part 2 with the actual input file."""
        if os.path.exists("input.txt"):
            result, invalid_ids = solve_part2("input.txt")
            self.assertEqual(result, 24774350322)
            self.assertEqual(len(invalid_ids), 889)


if __name__ == "__main__":
    unittest.main(verbosity=2)
