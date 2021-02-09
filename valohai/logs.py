import json
import sys

_supported_types = [int, float]


class logger(object):
    def __init__(self):
        self.partial_logs = {}

    def __enter__(self):
        self.partial_logs = {}
        return self

    def __exit__(self, type, value, traceback):
        self.flush_logs()

    def log(self, name, value):
        """Log a single name/value pair to be flushed into standard output later as batch.

        For a repeating iteration like a machine learning training loop, Valohai expects
        all logged values to be printed as a batch.

        Example:
            for epoch in range(10):
                with logger as valohai.logger():
                    logger.log("epoch", epoch)
                    logger.log("accuracy", 0.54)
                    logger.log("loss", 0.123)

        Example 2:
            for epoch in range(10):
                logger = valohai.logger():
                logger.log("epoch", epoch)
                logger.log("accuracy", 0.54)
                logger.log("loss", 0.123)
                logger.flush_logs()

        Both examples will log all three metrics at once at the end of each epoch.

        :param name: Name of the variable being logged (example: learning_rate)
        :param value: Value of the logged variable

        """
        serializable = self._get_serializable(name, value)
        if serializable:
            self.partial_logs.update(serializable)

    def flush_logs(self):
        """Flush all the partial logs into standard as a batch.

        For a repeating iteration like a machine learning training loop, Valohai expects
        all logged values to be printed as single batch.

        Example:
            logger = valohai.logger():
            logger.log("epoch", epoch)
            logger.log("accuracy", 0.54)
            logger.log("loss", 0.123)
            logger.flush_logs()

        This will log all three metrics at once.
        """
        if self.partial_logs:
            print(json.dumps(self.partial_logs))
            self.partial_logs.clear()

    def _get_serializable(self, name, value):
        if isinstance(value, (int, str, float)):
            return {str(name): value}

        print(f"Warning: Value of the logged item ({name}) is not of the expected type (int, str, float).",
              file=sys.stderr)
        return None
