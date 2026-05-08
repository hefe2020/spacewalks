

import pytest
from eva_data_analysis import text_to_duration, calculate_crew_size

def test_text_to_duration_float():
    """
    Test that text_to_duration returns expected ground truth values
    for typical durations with a non-zero minute component
    """
    assert text_to_duration("10:20") == pytest.approx(10.33333)


def test_text_to_duration_interger():
    """
    Test that text_to_duration returns expected ground truth values
    for typical whole hour duration
    """
    input_value = "10:00"
    assert text_to_duration(input_value) == 10


@pytest.mark.parametrize("input_value, expected_results", [
    ("valentina Teresh;", 1), 
    ("Judith Resnik; Sally bug;", 2)
    ])
def test_calculate_crew_size(input_value, expected_results):
    """
    Test the calculate_crew_size returns the number of the crew members
    """
    actual_results = calculate_crew_size(input_value)
    assert actual_results == expected_results

def test_calculate_crew_size_edge_cases():
    """
    Test it returns expected values for edge cases where crew is an empty string

    """
    actual_results = calculate_crew_size("")
    assert actual_results is None


