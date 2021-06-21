import valohai

params = {
    "param1": True,
    "param2": "asdf",
    "param3": 123,
    "param4": 0.0001,
}

inputs = {"input1": "asdf", "input2": ["yolol", "yalala"], "my-optional-input": ""}


def prepare(a, b):
    print(f"this is fake method {a} {b}")


valohai.prepare(step="foobar1", default_parameters=params, default_inputs=inputs)
