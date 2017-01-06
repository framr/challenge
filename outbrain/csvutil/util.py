
def get_column_index_mapping(header):
    """
    Zero based!
    Args:
        header:

    Returns:

    """
    mapping = dict((col, index) for index, col in enumerate(header))
    return mapping


def get_column_indices_from_header(columns, header):
    """
    Zero based!
    Args:
        columns:
        header:

    Returns:

    """
    column_index_mapping = get_column_index_mapping(header)
    indices = [column_index_mapping[column] for column in columns]
    return indices

