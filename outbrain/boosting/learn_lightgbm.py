import lightgbm as lgb
import pandas as pd
import numpy as np
import json


def get_dtypes(task, infile, separator=","):

    with open(infile) as f:
        header = f.readline().strip().split(separator)
    header = set(header)

    result = {}
    for f in task["factors"]:
        dtype = task["factors_types"].get(f, "float")

        if dtype == "int":
            result[f] = np.int32
        elif dtype == "float":
            result[f] = np.float64

    result[task["click_field"]] = np.int32
    if "group_field" in task:
        result[task["group_field"]] = np.int32

    extra_columns = header - set(result.keys())
    for col in extra_columns:
        result[col] = object

    #for key in result:
    #    result[key] = object

    return result


def learn_lightgbm(learn_file, task, test_file=None, separator=","):

    print "factors %s" % task["factors"]
    cut_fields = [task["click_field"]] + task["factors"]

    params = {"task": "train"}
    params.update(task["learn"]["lightgbm"])

    if task["learn"]["lightgbm"]["objective"] == "lambdarank":
        print "Training in the lambdarank regime with column %s used for grouping"\
            % task["group_field"]
        params.update({"group": "name:%s" % task["group_field"]})
        cut_fields.append(task["group_field"])

    print "LightGBM learning parameters: %s" % params

    print('Loading data')
    dtypes = get_dtypes(task, learn_file)
    #print cut_fields, dtypes

    df_train = pd.read_csv(learn_file, sep=separator, usecols=cut_fields, dtype=dtypes)
    if test_file:
        df_test = pd.read_csv(test_file, sep=separator, usecols=cut_fields, dtype=dtypes)

    y_train = df_train[task["click_field"]]
    X_train = df_train.drop(task["click_field"], axis=1)

    print "learn dataframe columns %s" % list(X_train.columns)
    if test_file:
        y_test = df_test[task["click_field"]]
        X_test = df_test.drop(task["click_field"], axis=1)
    print "done!"


    lgb_train = lgb.Dataset(X_train, y_train)
    lgb_eval = None

    if test_file:
        lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)


    print('Start training')
    gbm = lgb.train(params,
                    lgb_train,
                    valid_sets=lgb_eval,
    #                num_boost_round=20,
    #                early_stopping_rounds=5
    )

    print('Save model...')
    gbm.save_model('model.txt')

    y_train_pred = gbm.predict(X_train)
    with open("learn_predict.txt", "w") as outf:
        for el in y_train_pred:
            outf.write("%f\n" % el)

    if test_file:
        y_test_pred = gbm.predict(X_test)
        with open("test_predict.txt", "w") as outf:
            for el in y_test_pred:
                outf.write("%f\n" % el)

    #y_train_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)
    #print('The rmse of prediction is:', mean_squared_error(y_test, y_pred) ** 0.5)

    model_json = gbm.dump_model()
    with open('model.json', 'w+') as f:
        json.dump(model_json, f, indent=4)

    #print('Feature importances:', list(gbm.feature_importance()))
    #print('Feature importances:', list(gbm.feature_importance("gain")))
