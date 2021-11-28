import loguru
import tqdm


def loguru_set_verbosity(verbosity: int):
    """
    Set the verbosity of the tqdm logger.

    :param verbosity: 0 for >= INFO,
                      1 for >= DEBUG,
                      2 for >= TRACE
    """

    if verbosity == 0:
        level = "INFO"
    elif verbosity == 1:
        level = "DEBUG"
    elif verbosity >= 2:
        level = "TRACE"
    else:
        raise NotImplementedError(f"Unknown verbosity level -> {verbosity}")

    loguru.logger.remove()
    loguru.logger.add(
        sys.stderr,  # type: ignore
        format="{time:HH:mm:ss.SS} | {level} \t| {message}",
        level=level,
        colorize=True,
    )


def loguru_tqdm_sink(verbosity: int = 1):
    """Change the default loguru logger to use tqdm.

    :param verbosity: Set the verbosity of the tqdm logger.
                      0 for >= INFO,
                      1 for >= DEBUG,
                      2 for >= TRACE
    """
    if verbosity == 0:
        level = "INFO"
    elif verbosity == 1:
        level = "DEBUG"
    elif verbosity >= 2:
        level = "TRACE"
    else:
        raise NotImplementedError(f"Unknown verbosity level -> {verbosity}")

    loguru.logger.remove()
    loguru.logger.add(
        lambda msg: tqdm.tqdm.write(msg, end=""),  # type: ignore
        format="{time:HH:mm:ss.SS} | {level} \t| {message}",
        level=level,
        colorize=True,
    )
