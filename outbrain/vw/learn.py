from subprocess import check_call


class BasicLearner(object):
    pass

class VWLearner(BasicLearner):
    def __init__(self):
        pass


def get_vw_launch_args(task):

    # TODO: ADD QUADRATICS!!!
    vw_opts = task["learn"]["vw"]

    args = [vw_opts["binary"]]
    args.extend(["--cache_file", "./vw_cache"])
    args.extend(["-f", "./model"])
    args.extend(["--readable_model", "./rmodel"])
    #args.extend(["--invert_hash", "./rmodel_inverted_hash"])


    args.extend(["-b", vw_opts["num_bits"]])
    args.extend([vw_opts["learn_method"]])
    args.extend(["--loss_function", vw_opts["loss"]])

    if vw_opts.get("l1", None) is not None:
        args.extend(["--l1", vw_opts["l1"]])
    if vw_opts.get("l2", None) is not None:
        args.extend(["--l2", vw_opts["l2"]])

    args.extend(["--passes", vw_opts["passes"]])

    if vw_opts["manual_bias"]:
        args.extend(["--noconstant"])
    if vw_opts["learn_options"] is not None:
        args.extend([vw_opts["learn_options"]])

    if vw_opts["hashing_mode"] == "manual":
        args.extend(["--hash", "strings"])
    else:
        quad = task["learn"]["quadratic"]
        vw_quad_pairs = [
            "-q %s%s" % (
            task["learn"]["ns_rename"].get(first, first)[0],
            task["learn"]["ns_rename"].get(second, second)[0]
            )
                for first, second in quad]

        args.extend(vw_quad_pairs)

    return " ".join(map(str, args))


def learn_vw(learn_file, task):

    #logger = Logger()
    args = get_vw_launch_args(task)
    print "vw launch command %s" % args
    with open(learn_file) as infile:
        with open('./vw.stderr', 'w') as stderr_file:
            with open('./vw.stdout', 'w') as stdout_file:
                return_code = check_call(args, stdin=infile, stderr=stderr_file, stdout=stdout_file,
                                         shell=True)

    if return_code == 0:
        print "vw learned successfully"
        #logger.info("vowpal wabbit learned successfully")
    else:
        raise Exception("Learning vw error, return code = %s" % return_code)




