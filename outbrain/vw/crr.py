from itertools import groupby


from ..csvutil.reader import csv_file_iter


def preprocess_table_for_crr(infilename, outfilename, task):
    """
    Args:
        infilename: sorted by group key
        task:

    Returns:
    """
    pass


def expand_crr_pairs(examples_group, task):

    clicked_examples = []
    notclicked_examples = []

    for example in examples_group:
        if int(getattr(example, task['click_field'])) == 1:
            clicked_examples.append(example)
        else:
            notclicked_examples.append(example)

    for clicked in clicked_examples:
        for not_clicked in notclicked_examples:
            yield (clicked, not_clicked)



def calculate_crr_features():
    pass



