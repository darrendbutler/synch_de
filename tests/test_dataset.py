"""Test functions in dataset.py."""

import pytest

from synch_de import dataset
from tests.config import TEST_DATA_RETURN_1


# Test one function wiht multiple test cases
@pytest.mark.parametrize(
    "sample, expected_output", TEST_DATA_RETURN_1
)
def test_return_int(sample, expected_output):
    """
    Using this to try testing features.
    """

    assert expected_output == dataset.return_int(
        sample
    ), "expected output should be equal to the sample"


# Use one test case for multiple functions
@pytest.fixture
def example_data():
    "A piece of example data that can be used for multiple tests"
    # Pass the function name as an argument to another test function
    # when you want to use the data in that test function
    return "example data"
