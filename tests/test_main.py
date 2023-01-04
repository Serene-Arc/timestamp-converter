#!/usr/bin/env python3
# coding=utf-8

import re
from datetime import datetime
from pathlib import Path
from typing import Optional

import pytest

import timestampconverter.__main__ as main


@pytest.mark.parametrize(
    ("test_name", "test_regex_pattern", "expected"),
    (
        ("test", r"(\d)", None),
        ("2020", r"(\d*)", "2020"),
        ("2021_test", r"(\d*)", "2021"),
    ),
)
def test_extract_timestamp(test_name: str, test_regex_pattern: str, expected: Optional[str]):
    pattern = re.compile(test_regex_pattern)
    result = main.find_match_in_name(test_name, pattern)
    assert result == expected


@pytest.mark.parametrize(
    ("test_format_string", "test_time_string", "expected"),
    (
        ("%Y-%m-%d", "2021-04-22", datetime(2021, 4, 22)),
        ("%Y-%m-%d_%H-%M", "2021-04-22_10-20", datetime(2021, 4, 22, 10, 20)),
    ),
)
def test_convert_string_to_datetime(test_format_string: str, test_time_string: str, expected: datetime):
    result = main.convert_string_to_datetime(test_format_string, test_time_string)
    assert result == expected


@pytest.mark.parametrize(
    ("test_path_name", "test_old_str", "test_replacement_datetime", "expected"),
    (("test_old", "old", datetime(2021, 4, 22), "test_2021-04-22T00:00:00"),),
)
def test_calculate_new_name(
    test_path_name: str,
    test_old_str: str,
    test_replacement_datetime: datetime,
    expected: str,
    tmp_path: Path,
):
    test_path = Path(tmp_path, test_path_name)
    result = main.calculate_new_name(test_path, test_replacement_datetime, test_old_str)
    assert result.name == expected
