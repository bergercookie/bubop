import logging

import pytest
from _pytest.logging import caplog as _caplog  # type: ignore
from loguru import logger


@pytest.fixture
def caplog(_caplog):
    """
    Fixture that forwards loguru's output to std logging's output so that you can use caplog
    as usual
    """

    class PropogateHandler(logging.Handler):
        def emit(self, record):
            logging.getLogger(record.name).handle(record)

    logger.add(PropogateHandler(), format="{message}")
    yield _caplog
