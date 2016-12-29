import pytest


from outbrain.csvutil.reader import make_example_cls
from outbrain.vw.formatter import VWAutoFormatter, VWManualFormatter


@pytest.fixture()
def examples_vw_lines_task_fixture_for_autoformatter():
    example_cls = make_example_cls(["click", "ad_id", "document_id"])

    task = {
        "click_field": "click",
        "learn": {
            "vw": {"hashing_mode": "auto", "num_bits": 28, "manual_bias": False},
            "namespaces": ["ad_id", "document_id"],
            "quadratic": [],
            "cubic": []
        }
    }

    # list of tuples of the form (example converted to list, vw_line)
    data = [
        ([0, "1", "1"], "0 |ad_id 1|document_id 1"),
        ([0, "1", "2"], "0 |ad_id 1|document_id 2"),
        ([1, "5", "1 2 3 4 5"], "1 |ad_id 5|document_id 1 2 3 4 5")
    ]

    result = []
    for raw_example, vw_line in data:
        result.append((example_cls(*raw_example), vw_line))

    return result, task


@pytest.fixture()
def task1():
    return {
        "feature_map": "./tests/fixtures/feature_map1.csv",
        "click_field": "click",
        "learn": {
            "vw": {"hashing_mode": "manual", "num_bits": 25, "manual_bias": True},
            "namespaces": ["ad_id", "document_id"],
            "quadratic": [["ad_id", "document_id"]],
            "cubic": []
        }
    }

@pytest.fixture()
def feature_map1():
    fmap = {
        "ad_id": {
            "1": 11,
            "3": 33
#            "5" -> filtered
        },
        "document_id": {
            "1": 100,
            "2": 200
        },
        "ad_id^document_id": {
            "1^1": 100011,
            "1^2": 100012,
#            "3^1":, -> filtered
            "3^2": 100032
        }
    }

    return fmap


@pytest.fixture()
def examples_and_vw_lines_for_manualformatter_task1_feature_map1():
    example_cls = make_example_cls(["click", "ad_id", "document_id"])

    data = [
        ([0, "1 3", "1"], "0 | 11 33 100 100011 999"),
        ([0, "5", "2"], "0 | 200 999")
    ]

    result = []
    for raw_example, vw_line in data:
        result.append((example_cls(*raw_example), vw_line))

    return result



def test_vw_auto_formatter1(examples_vw_lines_task_fixture_for_autoformatter):

    data, task = examples_vw_lines_task_fixture_for_autoformatter

    formatter = VWAutoFormatter(task)
    for example, vw_line in data:
        result = formatter([example])
        assert result == vw_line


def test_vw_manual_formatter1(task1, examples_and_vw_lines_for_manualformatter_task1_feature_map1):

    formatter = VWManualFormatter(task1)
    for example, vw_line in examples_and_vw_lines_for_manualformatter_task1_feature_map1:
        result = formatter([example])
        assert result == vw_line









