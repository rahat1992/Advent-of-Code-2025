import unittest
import os
from solution import is_invalid_id, solve_part1


class TestGiftShop(unittest.TestCase):

    def test_is_invalid_id_simple_cases(self):
        """Test simple invalid IDs from the problem."""
        # Examples from the problem
        self.assertTrue(is_invalid_id(55))      # 5 twice
        self.assertTrue(is_invalid_id(6464))    # 64 twice
        self.assertTrue(is_invalid_id(123123))  # 123 twice

    def test_is_invalid_id_valid_cases(self):
        """Test valid IDs that should NOT be flagged."""
        self.assertFalse(is_invalid_id(101))    # Not a pattern repeated twice
        self.assertFalse(is_invalid_id(123))    # Odd length
        self.assertFalse(is_invalid_id(1234))   # 12 != 34
        self.assertFalse(is_invalid_id(100))    # Odd length

    def test_is_invalid_id_leading_zeros(self):
        """Test that numbers with leading zeros are not considered."""
        # 0101 shouldn't be an ID at all - but we're checking numeric values
        # so this would be 101 which is valid
        self.assertFalse(is_invalid_id(101))

    def test_is_invalid_id_from_example_ranges(self):
        """Test specific invalid IDs mentioned in the example."""
        self.assertTrue(is_invalid_id(11))          # from 11-22
        self.assertTrue(is_invalid_id(22))          # from 11-22
        self.assertTrue(is_invalid_id(99))          # from 95-115
        self.assertTrue(is_invalid_id(1010))        # from 998-1012
        self.assertTrue(is_invalid_id(1188511885))  # from 1188511880-1188511890
        self.assertTrue(is_invalid_id(222222))      # from 222220-222224
        self.assertTrue(is_invalid_id(446446))      # from 446443-446449
        self.assertTrue(is_invalid_id(38593859))    # from 38593856-38593862

    def test_range_11_to_22(self):
        """Test the range 11-22 has exactly 11 and 22 as invalid."""
        invalid_in_range = [num for num in range(11, 23) if is_invalid_id(num)]
        self.assertEqual(invalid_in_range, [11, 22])

    def test_range_95_to_115(self):
        """Test the range 95-115 has exactly 99 as invalid."""
        invalid_in_range = [num for num in range(95, 116) if is_invalid_id(num)]
        self.assertEqual(invalid_in_range, [99])

    def test_range_998_to_1012(self):
        """Test the range 998-1012 has exactly 1010 as invalid."""
        invalid_in_range = [num for num in range(998, 1013) if is_invalid_id(num)]
        self.assertEqual(invalid_in_range, [1010])

    def test_range_1698522_to_1698528(self):
        """Test the range 1698522-1698528 contains no invalid IDs."""
        invalid_in_range = [num for num in range(1698522, 1698529) if is_invalid_id(num)]
        self.assertEqual(invalid_in_range, [])

    def test_example_input(self):
        """Test with the example from the problem."""
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

    def test_four_digit_patterns(self):
        """Test various 4-digit patterns."""
        self.assertTrue(is_invalid_id(1010))
        self.assertTrue(is_invalid_id(2020))
        self.assertTrue(is_invalid_id(3030))
        self.assertTrue(is_invalid_id(9999))
        self.assertFalse(is_invalid_id(1020))
        self.assertFalse(is_invalid_id(1234))

    def test_six_digit_patterns(self):
        """Test various 6-digit patterns."""
        self.assertTrue(is_invalid_id(123123))
        self.assertTrue(is_invalid_id(456456))
        self.assertTrue(is_invalid_id(999999))
        self.assertFalse(is_invalid_id(123456))
        self.assertFalse(is_invalid_id(111222))

    def test_single_digit_repeated(self):
        """Test single digits repeated."""
        for digit in range(1, 10):  # 1-9 (not 0 due to leading zero rule)
            num_str = str(digit) * 2
            self.assertTrue(is_invalid_id(int(num_str)))

    def test_odd_length_numbers(self):
        """Test that odd-length numbers are never invalid."""
        self.assertFalse(is_invalid_id(1))
        self.assertFalse(is_invalid_id(123))
        self.assertFalse(is_invalid_id(12345))
        self.assertFalse(is_invalid_id(1234567))

    def test_actual_input(self):
        """Test with the actual input file."""
        if os.path.exists("input.txt"):
            result, invalid_ids = solve_part1("input.txt")
            self.assertEqual(result, 12850231731)
            self.assertEqual(len(invalid_ids), 807)


if __name__ == "__main__":
    unittest.main(verbosity=2)
