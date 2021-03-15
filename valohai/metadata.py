import json

_supported_types = [int, float]


class Logger:
    def __init__(self):
        self.partial_logs = {}

    def __enter__(self):
        self.partial_logs = {}
        return self

    def __exit__(self, type, value, traceback):
        self.flush()

    def log(self, *args, **kwargs):
        """Log a single name/value pair to be flushed into standard output later as batch.

        For a repeating iteration like a machine learning training loop, Valohai expects
        all logged values to be printed as a batch.

        Example:
            for epoch in range(10):
                with valohai.logger() as logger:
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

        Example 3:
            for epoch in range(10):
                with valohai.logger() as logger:
                    logger.log("epoch", epoch)
                    logger.log(acc=0.54, loss=0.123)

        All three examples will act exactly the same.

        :param name: Name of the variable being logged (example: learning_rate)
        :param value: Value of the logged variable

        """
        if len(args) % 2 != 0:
            raise ValueError(f"Odd number of arguments in {args} for log()")
        for key, value in zip(args[::2], args[1::2]):
            self._serialize(key, value)
        for key, value in kwargs.items():
            self._serialize(key, value)

    def flush(self):
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
            print(json.dumps(self.partial_logs, default=str))
            self.partial_logs.clear()

    def _serialize(self, name, value):
        self.partial_logs.update({str(name): value})


logger = Logger
