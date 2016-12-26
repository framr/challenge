import pytest


from outbrain.csvutil.reader import make_example_cls
from outbrain.vw.formatter import VWAutoFormatter



@pytest.fixture()
def task1():
    return {
        "click_field": "click",
        "learn": {
            "namespaces": ["ad_id", "document_id"],
            "quadratic": [],
            "cubic": []
        }
    }


@pytest.fixture()
def examples_and_vw_lines_task1():
    example_cls = make_example_cls(["click", "ad_id", "document_id"])

    data = [
        ([0, "1", "1"], "0 |ad_id 1|document_id 1"),
        ([0, "1", "2"], "0 |ad_id 1|document_id 2"),
        ([1, "5", "1 2 3 4 5"], "1 |ad_id 5|document_id 1 2 3 4 5")
    ]

    result = []
    for raw_example, vw_line in data:
        result.append((example_cls(*raw_example), vw_line))

    return result



def test_vw_auto_formatter1(task1, examples_and_vw_lines_task1):

    formatter = VWAutoFormatter(task1)
    for example, vw_line in examples_and_vw_lines_task1:
        result = formatter([example])
        assert result == vw_line







