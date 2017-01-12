import lightgbm as lgb
import pandas as pd
import numpy as np
import json


def learn_lightgbm(learn_file, task, test_file=None, separator=","):

    print "factors %s" % task["factors"]
    cut_fields = task["click_field"] + task["factors"]

    params = {"task": "train"}
    params.update(task["learn"]["lightgbm"])

    if task["learn"]["lightgbm"]["objective"] == "lambdarank":
        print "Training in the lambdarank regime with column %s used for grouping"\
            % task["group_field"]
        params.update({"group": "name:%s" % task["group_field"]})
        cut_fields.append(task["group_field"])

    print "LightGBM learning parameters: %s" % params

    print('Loading data')
    df_train = pd.read_csv(learn_file, sep=separator, names=cut_fields)
    if test_file:
        df_test = pd.read_csv(test_file, sep=separator, names=)

    y_train = df_train[task["click_field"]]
    X_train = df_train.drop(task["click_field"], axis=1)
    if test_file:
        y_test = df_test[task["click_field"]]
        X_test = df_train.drop(task["click_field"], axis=1)
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
    with open("learn_predict.txt") as outf:
        for el in y_train_pred:
            outf.write("%f\n" % el)

    if test_file:
        y_test_pred = gbm.predict(X_test)
        with open("test_predict.txt") as outf:
            for el in y_test_pred:
                outf.write("%f\n" % el)

    #y_train_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)
    #print('The rmse of prediction is:', mean_squared_error(y_test, y_pred) ** 0.5)


    model_json = gbm.dump_model()
    with open('model.json', 'w+') as f:
        json.dump(model_json, f, indent=4)

    #print('Feature importances:', list(gbm.feature_importance()))
    #print('Feature importances:', list(gbm.feature_importance("gain")))