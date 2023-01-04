#!/usr/bin/env python3

import argparse
import logging
import os
import platform
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

parser = argparse.ArgumentParser()
logger = logging.getLogger()


def _setup_logging(verbosity: int):
    logger.setLevel(1)
    stream = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("[%(asctime)s - %(name)s - %(levelname)s] - %(message)s")
    stream.setFormatter(formatter)
    logger.addHandler(stream)
    if verbosity > 0:
        stream.setLevel(logging.DEBUG)
    else:
        stream.setLevel(logging.INFO)


def _add_arguments():
    parser.add_argument("destination", type=str)
    parser.add_argument("regex", type=str)
    parser.add_argument("timeformat", type=str)
    recursive = parser.add_mutually_exclusive_group()

    recursive.add_argument("-r", "--recursive", action="store_true")
    recursive.add_argument("--include-folders", action="store_true")
    parser.add_argument("-n", "--no-act", action="store_true")
    parser.add_argument("-v", "--verbose", action="count", default=0)


def main(args: argparse.Namespace):
    _setup_logging(args.verbose)
    args.destination = Path(args.destination).resolve().expanduser()
    directory_contents = []

    if args.recursive:
        for dirpath, dirnames, filenames in os.walk(args.destination):
            directory_contents.extend([Path(dirpath, filename).resolve() for filename in filenames])
            directory_contents.extend([Path(dirpath, dirname).resolve() for dirname in dirnames])
    else:
        contents = list(args.destination.iterdir())
        directory_contents.extend(contents)

    if not args.include_folders:
        directory_contents = list(filter(lambda f: f.is_file, directory_contents))

    logger.info(f"{len(directory_contents)} files found")
    regex = re.compile(args.regex)
    for file in directory_contents:
        match_text = find_match_in_name(file.name, regex)
        if not match_text:
            continue
        file_time = convert_string_to_datetime(args.timeformat, match_text)
        if not file_time:
            continue
        new_path = calculate_new_name(file, file_time, match_text)
        if args.no_act:
            print(f"{file} -> {new_path}")
        else:
            file.rename(new_path)
            logger.info(f"Renamed {file} to {new_path}")


def calculate_new_name(file: Path, file_time: datetime, match_text: str) -> Path:
    new_name = file.name.replace(match_text, file_time.isoformat())
    if platform.system() == "Windows":
        new_name = new_name.replace(":", "")
    new_path = Path(file.parent, new_name)
    return new_path


def convert_string_to_datetime(time_format: str, match_text: str) -> Optional[datetime]:
    try:
        file_time = datetime.strptime(match_text, time_format)
        return file_time
    except ValueError:
        logger.error(f"Regex match {match_text} was not compatible with given time format")


def find_match_in_name(file_name: str, regex: re.Pattern) -> Optional[str]:
    match = re.search(regex, file_name)
    if not match:
        logger.debug(f"No regex match found in {file_name}")
        return None
    match_text = match.group()
    return match_text


if __name__ == "__main__":
    _add_arguments()
    args = parser.parse_args()
    main(args)
