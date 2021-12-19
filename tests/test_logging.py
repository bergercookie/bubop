from loguru import logger

from bubop import logger, loguru_set_verbosity


def test_loguru_set_verbosity(caplog):
    logger.debug("kalimera")
    loguru_set_verbosity(0)
    logger.debug("kalinuxta")
    captured = caplog.text
    assert "kalimera" in captured
    assert "kalinuxta" not in captured
