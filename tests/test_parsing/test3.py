import valohai

valohai.prepare(
    step="foobar3",
    default_parameters={"param1": True, "param2": "asdf", "param3": 123, "param4": 0.0001},
    default_inputs={"input1": "asdf", "input2": ["yolol", "yalala"]},
)
