import valohai


def test_basic_logging(capsys):
    with valohai.logger() as logger:
        logger.log("myint", 123)
    captured = capsys.readouterr()
    assert captured.out == "{\"myint\": 123}\n"

    with valohai.logger() as logger:
        logger.log("I am float", 0.1241234435877)
    captured = capsys.readouterr()
    assert captured.out == "{\"I am float\": 0.1241234435877}\n"


def test_logging_with_unsupported_types(capsys):
    with valohai.logger() as logger:
        logger.log("herp", ["asdif", 234, None])
    captured, err = capsys.readouterr()
    assert "Warning: Value of the logged item (herp) is not of the expected type (int, str, float)." in err


def test_partial_logging(capsys):
    with valohai.logger() as logger:
        logger.log("myint", 123)
        logger.log("myfloat", 0.5435)
    captured = capsys.readouterr()
    assert captured.out == "{\"myint\": 123, \"myfloat\": 0.5435}\n"

    logger = valohai.logger()
    logger.log("myint", 234)
    logger.log("myfloat", 0.2322323)
    logger.log("extrathing", 2)
    logger.flush_logs()
    captured = capsys.readouterr()
    assert captured.out == "{\"myint\": 234, \"myfloat\": 0.2322323, \"extrathing\": 2}\n"
