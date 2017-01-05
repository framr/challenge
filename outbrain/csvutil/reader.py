import csv
from collections import namedtuple
from itertools import groupby

from .util import get_column_index_mapping


def make_example_cls(fields):
    Example = namedtuple('Example', fields)
    return Example


def csv_file_iter(infile):
    """
    Args:
        infile: open file

    Returns:

    """
    meta = infile.readline().strip()
    example_cls = make_example_cls(meta)
    for line in csv.reader(infile):
        yield example_cls(*line)


def csv_file_group_iter(infile, group_field):
    meta = infile.readline().strip()
    example_cls = make_example_cls(meta)

    group_field_index = get_column_index_mapping(meta)[group_field]
    for group_key, group_iter in groupby(csv.reader(infile),
                                         key=lambda row: row[group_field_index]):

        examples = [example_cls(*row) for row in group_iter]
        yield group_key, examples


def csv_file_extended_iter(infile):
    """
    Args:
        infile: open file

    Returns:

    """

    # Copypaste, looks ugly
    meta = infile.readline().strip()
    example_cls = make_example_cls(meta)
    for line in csv.reader(infile):
        yield line, example_cls(*line)

