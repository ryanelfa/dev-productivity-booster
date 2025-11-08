import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from main import calculate_score, load_dataset
import pandas as pd
from pathlib import Path

def test_calculate_score():
    # Create a mock row with sample data
    row = pd.Series({
        "commits": 10,
        "tests_passed": 8,
        "bugs_fixed": 5,
        "lines_added": 200
    })

    # Call the calculate_score function
    score = calculate_score(row)

    # Assert that the score is a positive float
    assert isinstance(score, float)
    assert score > 0

def test_load_dataset(tmp_path):
    # Create a temporary CSV file with valid data
    csv_content = "developer,commits,tests_passed,bugs_fixed,lines_added\n"
    csv_content += "dev1,10,8,5,200\n"
    csv_content += "dev2,15,10,7,300\n"
    temp_file = tmp_path / "Productivity.csv"
    temp_file.write_text(csv_content)

    # Call the load_dataset function
    df = load_dataset(temp_file)

    # Assert that the dataframe is loaded correctly
    assert not df.empty
    assert set(df.columns) == {"developer", "commits", "tests_passed", "bugs_fixed", "lines_added"}
    assert len(df) == 2

