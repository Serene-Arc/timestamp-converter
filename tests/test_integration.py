#!/usr/bin/env python3
# coding=utf-8

from argparse import Namespace
from pathlib import Path

import pytest

import timestampconverter.__main__ as main


@pytest.fixture()
def args(tmp_path: Path) -> Namespace:
    args = Namespace()
    args.destination = tmp_path
    args.include_folders = False
    args.no_act = False
    args.recursive = False
    args.regex = ''
    args.timeformat = ''
    args.verbose = 1
    return args


def test_rename_files(args: Namespace, capsys: pytest.CaptureFixture):
    args.timeformat = '%Y-%m-%d_%H-%M'
    args.regex = r'(\d{4}-\d{2}-\d{2}_\d{2}-\d{2})'
    for i in range(0, 4):
        Path(args.destination, f'2021-04-20_17-49_test_{i}.png').touch()
    main.main(args)
    output = capsys.readouterr()
    assert all([Path(args.destination, f'2021-04-20T17:49:00_test_{i}.png').exists() for i in range(0, 4)])
    assert 'Renamed' in output.out


def test_rename_files_no_act(args: Namespace, capsys: pytest.CaptureFixture):
    args.no_act = True
    args.timeformat = '%Y-%m-%d_%H-%M'
    args.regex = r'^(\d{4}-\d{2}-\d{2}_\d{2}-\d{2})'
    create_test_files(args)
    main.main(args)
    output = capsys.readouterr()
    assert all([Path(args.destination, f'2021-04-20_17-49_test_{i}.png').exists() for i in range(0, 4)])
    assert 'Renamed' not in output.out
    assert '.png ->' in output.out


def create_test_files(args):
    for i in range(0, 4):
        Path(args.destination, f'2021-04-20_17-49_test_{i}.png').touch()
