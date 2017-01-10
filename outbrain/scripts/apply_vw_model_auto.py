#!/usr/bin/env python
import os
import yaml
from argparse import ArgumentParser
from tempfile import NamedTemporaryFile

from outbrain.vw.apply import VWAutoPredictor, merge_predictions

if __name__ == "__main__":

    argparser = ArgumentParser()
    argparser.add_argument("-f", dest="formatted", type=str, default=None, help="vw formatted input file")
    argparser.add_argument("-i", dest="input", type=str, default=None, help="original input file")
    argparser.add_argument("-o", dest="output", type=str, default=None, help="output file")
    argparser.add_argument("--model", dest="model_path", type=str, default=None, help="path with vw model")
    argparser.add_argument("--target", dest="target", type=str, default="vw", help="target field")
    args = argparser.parse_args()

    task_file = os.path.join(args.model_path, "task.yml")
    model_file = os.path.join(args.model_path, "model")
    task = yaml.load(open(task_file).read())
    predictor = VWAutoPredictor(model_file)

    with NamedTemporaryFile(delete=True) as tmp_file:
        predictor.apply(args.formatted, tmp_file.name)
        merge_predictions(args.input, tmp_file.name, args.output, target=args.target)

