import csv
from collections import namedtuple


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
        yield example_cls(line)

