from logging import Logger
from subprocess import check_call
from math import exp

class VWPredictor(object):
    def __init__(self, model_path):
        pass
    def apply(self, learn_log):
        pass
    def prediction_for_example(self, example):
        pass



class VWAutoPredictor(VWPredictor):

    def __init__(self, model_path, task=None, mbus=None):
        self._model_path = model_path
        self._task = None
        self._mbus = None

    def apply(self, learn_log, output_log):

        #logger = Logger()

        vw_args = ["vw", learn_log, "-t"]
        vw_args.extend(["-i", self._model_path])
        vw_args.extend(["-p", output_log])
        vw_cmd = " ".join(map(str, vw_args))

        print "vowpal wabbit launch command %s" % vw_cmd

        with open("vw_predict.stderr", "w") as stderr_file:
            with open("vw_predict.stdout", "w") as stdout_file:
                return_code = check_call(vw_cmd, stderr=stderr_file, stdout=stdout_file,
                                         shell=True)

        if return_code == 0:
            print "vowpal wabbit predictions successfully finished"
        else:
            raise Exception("vowpal wabbit predictions failed, return code = %s" % return_code)


    def prediction_for_example(self, example):
        raise NotImplementedError



class VWManualPredictor(VWPredictor):
    def __init__(self, model_path):
        raise NotImplementedError



def merge_predictions(original_file, pred_file, result_file, target="vw",
                      apply_sigmoid=True):

    with open(result_file, "w") as result:
        with open(original_file) as original:
            with open(pred_file)as predictions:
                header = original.readline().strip()
                new_header = "%s,%\n" % (header, target)
                result.write(new_header)

                for line in original:
                    prediction = predictions.readline().strip()

                    result.write("%s,%s" % (line.strip(), prediction))
                    if apply_sigmoid:
                        result.write(",%s" % 1.0 / (1.0 + exp(-float(prediction))))
                    result.write("\n")



def apply_vw(infile):
    pass


def predict(example):
    pass




