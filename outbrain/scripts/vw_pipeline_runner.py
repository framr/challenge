#!/usr/bin/env python
"""
We have two posible pipelines here

1) compute feature stats [optional]
2) convert log into vw format using VWAutoFormatter [using optional feature stats fo filtering features]
3) run vw
4) compute metrics on train and test


1) compute feature stats [optional]
1) compute feature map [optionally filtering it using feature stats]
2) convert log into vw format using VWManualFormatter [using optional feature stats fo filtering features]
3) run vw
4) compute metrics on train and test
"""


from outbrain.vw.action import *


def run_pipeline(task):
    pass