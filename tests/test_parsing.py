from valohai.internals.parsing import parse


def test_parameters_parse(source_codes):
    for test_item in source_codes:
        step, params, inputs = parse(test_item['source'])
        assert params == test_item['parameters']
        assert inputs == test_item['inputs']
        assert step == test_item["step"]['name']
