from logging import Logger
from subprocess import check_call


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

        logger = Logger()

        vw_args = ["vw", "-t"]
        vw_args.extend(["-i", learn_log])
        vw_args.extend(["-p", self._model_path])
        vw_cmd = " ".join(map(str, vw_args))

        logger.info("vowpal wabbit launch command")

        with open("vw_predict.stderr", "w") as stderr_file:
            with open("vw_predict.stdout", "w") as stdout_file:
                return_code = check_call(vw_cmd, stderr=stderr_file, stdout=stdout_file,
                                         shell=True)

        if return_code == 0:
            logger.info("vowpal wabbit predictions successfully finished")
        else:
            raise Exception("vowpal wabbit predictions failed, return code = %s" % return_code)


    def prediction_for_example(self, example):
        raise NotImplementedError



class VWManualPredictor(VWPredictor):
    def __init__(self, model_path):
        raise NotImplementedError



def apply_vw(infile):
    pass


def predict(example):
    pass




