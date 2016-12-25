from itertools import groupby


def preprocess_table_for_crr(filename, task):
    """
    Args:
        filename: sorted by group key
        task:

    Returns:

    """

    pass



def emit_crr_pairs(group, task):

    clicked_examples = []
    notclicked_examples = []

    for example in group:
        if int(getattr(example, task['click_field'])) == 1:
            clicked_examples.append(example)
        else:
            notclicked_examples.append(example)

    for clicked in clicked_examples:
        for not_clicked in notclicked_examples:
            pass




