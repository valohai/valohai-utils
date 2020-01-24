from valohai.internals.parsing import parse


def test_parameters_parse(source_codes):
    for test_item in source_codes:
        print(test_item['source'])
        result = parse(test_item['source'])

        assert result.parameters == test_item['parameters']
        assert result.inputs == test_item['inputs']
        assert result.step == test_item["step"]['name']
