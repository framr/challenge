#!/usr/bin/env python
import yaml
from argparse import ArgumentParser


from outbrain.boosting.learn_lightgbm import learn_lightgbm


if __name__ == "__main__":

    argparser = ArgumentParser()
    argparser.add_argument("-i", dest="learn", type=str, default=None, help="learn file", required=True)
    argparser.add_argument("-t", dest="test", type=str, default=None, help="test file")
    argparser.add_argument("--task", dest="task", default=None, type=str, help="task file",
                           required=True)
    args = argparser.parse_args()

    task = yaml.load(open(args.task).read())


    learn_lightgbm(args.learn,
                   task,
                   test_file=args.test
    )




