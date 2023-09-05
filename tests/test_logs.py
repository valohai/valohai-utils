import io
import sys

import valohai


def test_basic_logging(capsys, monkeypatch):
    with valohai.logger() as logger:
        logger.log("myint", 123)
    captured = capsys.readouterr()
    assert captured.out == '\n{"myint": 123}\n'

    with monkeypatch.context() as m:
        m.setenv("VALOHAI_PORT", 1234)
        with valohai.logger() as logger:
            logger.log("with_port", True)
        captured = capsys.readouterr()
        assert captured.out == '\n{"vh_metadata": {"with_port": true}}\n'

    with valohai.logger() as logger:
        logger.log("I am float", 0.1241234435877)
    captured = capsys.readouterr()
    assert captured.out == '\n{"I am float": 0.1241234435877}\n'


def test_partial_logging(capsys):
    with valohai.logger() as logger:
        logger.log("myint", 123)
        logger.log("myfloat", 0.5435)
    captured = capsys.readouterr()
    assert captured.out == '\n{"myint": 123, "myfloat": 0.5435}\n'

    logger = valohai.logger()
    logger.log("myint", 234)
    logger.log("myfloat", 0.2322323)
    logger.log("extrathing", 2)
    logger.flush()
    captured = capsys.readouterr()
    assert captured.out == '\n{"myint": 234, "myfloat": 0.2322323, "extrathing": 2}\n'


def test_redirected_logs(monkeypatch):
    out = io.StringIO()
    fake_out = io.StringIO()
    monkeypatch.setenv("JPY_PARENT_PID", "1234")  # Pretend we're in a notebook...
    monkeypatch.setattr(sys, "__stdout__", out)
    monkeypatch.setattr(sys, "stdout", fake_out)
    with valohai.logger() as logger:
        logger.log("myint", 123)
    # didn't get written to the redirected output?
    assert not fake_out.getvalue()
    # but did get written to the original stdout?
    assert out.getvalue() == '\n{"myint": 123}\n'
