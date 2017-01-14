import csv
from collections import namedtuple
from itertools import groupby

from attrdict import AttrDict

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


def csv_file_group_iter(infile, group_field, separator=","):
    """
    Args:
        infile:
        group_field:
        separator:

    Returns:
    """

    # TODO: support multi-field keys
    meta = infile.readline().strip()
    example_cls = make_example_cls(meta)

    group_field_index = get_column_index_mapping(meta.split(separator))[group_field]
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


def csv_file_group_iter_mutable(infile, group_field, separator=",", replace_header=("^", "_")):
    """
    Args:
        infile:
        group_field:
        separator:

    Returns:
    """

    # TODO: support multi-field keys
    header = infile.readline().strip().split(separator)

    if replace_header:
        header = [col.replace(replace_header[0], replace_header[1]) for col in header]

    group_field_index = get_column_index_mapping(header)[group_field]
    for group_key, group_iter in groupby(csv.reader(infile),
                                         key=lambda row: row[group_field_index]):

        examples = [AttrDict(dict(zip(header, row))) for row in group_iter]
        #for row in group_iter:
        #    print dict(zip(header, row))
        #    print AttrDict(dict(zip(header, row)))
        #examples = []

        #for e in examples:
        #    print e
        yield group_key, examples

