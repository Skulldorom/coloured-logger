import io
import logging
import unittest

from coloured_logger import ColouredFormatter, setup_logging


class FormatterTests(unittest.TestCase):
    def test_formatter_without_color(self):
        formatter = ColouredFormatter(use_color=False, datefmt="%Y")
        record = logging.LogRecord("test", logging.INFO, __file__, 1, "hello", (), None)
        output = formatter.format(record)
        self.assertIn("[INFO] hello", output)
        self.assertNotIn("\033[", output)

    def test_logger_adds_success_level_output(self):
        stream = io.StringIO()
        logger = setup_logging(
            logger_name="coloured_logger_test",
            level=logging.DEBUG,
            stream=stream,
            use_color=False,
            datefmt="%Y",
        )
        logger.success("done")
        value = stream.getvalue()
        self.assertIn("[SUCCESS] done", value)


if __name__ == "__main__":
    unittest.main()
