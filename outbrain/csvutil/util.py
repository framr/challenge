from .reader import csv_file_extended_iter


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


def generate_train_test_by_expression(infilename, train_expr, test_expr,
                                      train_filename, test_filename, separator=","):
    """
    Split file by train and test evaluating user expression returning True or False
    Example of expressions
    test_expr:
    int(example.document_id) % 4 == 0
    train_expr:
    int(example.document_id % 4) != 0

    Args:
        infilename:
        train_expr:
        test_expr:
        outfilename:
        separator:

    Returns:
    """

    test_expr_code = compile(test_expr, "<string>", "eval")
    train_expr_code = compile(train_expr, "<string>", "eval")

    train_examples_count = 0
    test_examples_count = 0
    with open(test_filename, "w") as outfile_test:
        with open(train_filename, "w") as outfile_train:

            with open(infilename) as infile:

                header = infile.readline()
                outfile_test.write(header)
                outfile_train.write(header)

                infile.seek(0, 0) # header is required once again in csv iter
                for line, example in csv_file_extended_iter(infile):
                    is_train = eval(train_expr_code, globals(), locals())
                    is_test = eval(test_expr_code, globals(), locals()  )

                    if is_test and is_train:
                        raise ValueError("Duplicating example in train and test forbidden")

                    if is_test:
                        test_examples_count += 1
                        outfile_test.write("%s\n" % separator.join(line))
                    if is_train:
                        train_examples_count += 1
                        outfile_train.write("%s\n" % separator.join(line))

    print "%d examples in train, %d examples in test" % (train_examples_count, test_examples_count)




