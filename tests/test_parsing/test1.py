import pandas as pd

import valohai

params = {
    "param1": True,
    "param2": "asdf",
    "param3": 123,
    "param4": 0.0001,
}

inputs = {"input1": "asdf", "input2": ["yolol", "yalala"]}


def prepare(a, b):
    print(f"this is fake method {a} {b}")


# Assignment that can't be evaluated (and should be ignored) by AST parser
foobar = pd.read_csv("yeah.csv")
prepare("this should not be parsed", "ever")
valohai.utils.prepare(step="this should not be parsed either")
valohai.prepare(step="foobar1", default_parameters=params, default_inputs=inputs)
