#!/usr/bin/env python

"""
Example usage
./generate_train_test.py -i ./fixtures/train.csv  --train ./fixtures/tmp_train --test ./fixtures/tmp_test --train-expr "int(example.display_id) % 2 == 1" --test-expr "int(example.display_id) % 2 == 0"
"""


from argparse import ArgumentParser
import yaml

from outbrain.csvutil.util import generate_train_test_by_expression


CONFIG_PARAMETERS = ["infile", "train", "test", "train_expr", "test_expr", "exec"]

def update_config(config, argparser):
    for par in CONFIG_PARAMETERS:
        if getattr(argparser, par) is not None:
            config[par] = getattr(argparser, par)


if __name__ == '__main__':

    argparser = ArgumentParser()
    argparser.add_argument("-i", dest="infile", type=str, default=None,
                           help="input file")
    argparser.add_argument("--train", dest="train", type=str, default=None,
                           help="train output file")
    argparser.add_argument("--test", dest="test", type=str, default=None,
                        help="test output file")

    argparser.add_argument("--train-expr", dest="train_expr", type=str, default=None,
                           help="train output file")
    argparser.add_argument("--test-expr", dest="test_expr", type=str, default=None,
                           help="test output file")

    argparser.add_argument("--exec", dest="exec", type=str, default=None,
                           help="exec expression")

    argparser.add_argument("--conf", dest="config", type=str, default=None, help="optional config file")


    config = dict((par, None) for par in CONFIG_PARAMETERS)
    args = argparser.parse_args()

    if args.config is not None:
        config = yaml.load(open(args.config).read())

    update_config(config, args) # optionally update config from provided command line arguments

    generate_train_test_by_expression(
        config["infile"],
        config["train_expr"],
        config["test_expr"],
        config["train"],
        config["test"],
        exec_expr=config["exec"]
    )



