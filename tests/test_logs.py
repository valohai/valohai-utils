from valohai.logs import flush_logs, log, log_partial


def test_basic_logging(capsys):
    log("myint", 123)
    captured = capsys.readouterr()
    assert captured.out == "{\"myint\": 123}\n"

    log("I am float", 0.1241234435877)
    captured = capsys.readouterr()
    assert captured.out == "{\"I am float\": 0.1241234435877}\n"


def test_logging_with_unsupported_types(capsys):
    log("herp", ["asdif", 234, None])
    captured, err = capsys.readouterr()
    assert "Warning: Value of the logged item (herp) is not of the expected type (int, str, float)." in err


def test_partial_logging(capsys):
    log_partial("myint", 123)
    log_partial("myfloat", 0.5435)
    flush_logs()
    captured = capsys.readouterr()
    assert captured.out == "{\"myint\": 123, \"myfloat\": 0.5435}\n"

    log_partial("myint", 234)
    log_partial("myfloat", 0.2322323)
    log_partial("extrathing", 2)
    flush_logs()
    captured = capsys.readouterr()
    assert captured.out == "{\"myint\": 234, \"myfloat\": 0.2322323, \"extrathing\": 2}\n"
