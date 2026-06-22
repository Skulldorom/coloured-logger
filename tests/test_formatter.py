import io
import logging
import os
import unittest

from coloured_logger import ColouredFormatter, SUCCESS_LEVEL, get_logger, setup_logging


class ColouredFormatterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Register the SUCCESS level name so direct formatter usage sees "SUCCESS"
        if logging.getLevelName(SUCCESS_LEVEL) != "SUCCESS":
            logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")

    def test_format_without_color(self):
        formatter = ColouredFormatter(use_color=False, datefmt="%Y")
        record = logging.LogRecord("test", logging.INFO, __file__, 1, "hello", (), None)
        output = formatter.format(record)
        self.assertIn("[INFO] hello", output)
        self.assertNotIn("\033[", output)

    def test_format_with_color(self):
        formatter = ColouredFormatter(use_color=True, datefmt="%Y")
        record = logging.LogRecord("test", logging.INFO, __file__, 1, "hello", (), None)
        output = formatter.format(record)
        self.assertIn("[INFO] hello", output)
        self.assertIn("\033[", output)

    def test_all_log_levels_have_colors(self):
        levels = {
            logging.DEBUG: "DEBUG",
            logging.INFO: "INFO",
            SUCCESS_LEVEL: "SUCCESS",
            logging.WARNING: "WARNING",
            logging.ERROR: "ERROR",
            logging.CRITICAL: "CRITICAL",
        }
        for levelno, levelname in levels.items():
            formatter = ColouredFormatter(use_color=True)
            record = logging.LogRecord("test", levelno, __file__, 1, "msg", (), None)
            output = formatter.format(record)
            self.assertIn(f"[{levelname}] msg", output)
            self.assertIn("\033[", output)

    def test_unknown_level_returns_uncolored(self):
        formatter = ColouredFormatter(use_color=True)
        record = logging.LogRecord("test", 99, __file__, 1, "msg", (), None)
        output = formatter.format(record)
        self.assertIn("[Level 99] msg", output)
        self.assertNotIn("\033[", output)

    def test_default_date_format(self):
        formatter = ColouredFormatter(use_color=False)
        self.assertEqual(formatter.datefmt, "%d/%m/%Y %H:%M:%S")

    def test_custom_date_format(self):
        formatter = ColouredFormatter(datefmt="%H:%M", use_color=False)
        self.assertEqual(formatter.datefmt, "%H:%M")

    def test_default_message_format(self):
        formatter = ColouredFormatter(use_color=False)
        self.assertEqual(formatter._fmt, "[%(asctime)s] [%(levelname)s] %(message)s")

    def test_custom_message_format(self):
        formatter = ColouredFormatter(fmt="%(levelname)s: %(message)s", use_color=False)
        self.assertEqual(formatter._fmt, "%(levelname)s: %(message)s")


class SetupLoggingTests(unittest.TestCase):
    def _make_stream_logger(self, **kwargs):
        stream = io.StringIO()
        logger = setup_logging(stream=stream, use_color=False, datefmt="%Y", **kwargs)
        return logger, stream

    def test_default_level_is_notset(self):
        logger, _ = self._make_stream_logger(logger_name="test_notset")
        self.assertEqual(logger.level, logging.NOTSET)

    def test_custom_level(self):
        logger, _ = self._make_stream_logger(logger_name="test_level_warn", level=logging.WARNING)
        self.assertEqual(logger.level, logging.WARNING)

    def test_handler_deduplication(self):
        logger1 = setup_logging(logger_name="test_dedup", use_color=False)
        count1 = len(logger1.handlers)
        logger2 = setup_logging(logger_name="test_dedup", use_color=False)
        count2 = len(logger2.handlers)
        self.assertEqual(count1, count2)
        self.assertGreaterEqual(count1, 1)

    def test_success_level_output(self):
        logger, stream = self._make_stream_logger(
            logger_name="test_success", level=logging.DEBUG
        )
        logger.success("done")
        value = stream.getvalue()
        self.assertIn("[SUCCESS] done", value)

    def test_debug_output(self):
        logger, stream = self._make_stream_logger(
            logger_name="test_debug", level=logging.DEBUG
        )
        logger.debug("trace")
        self.assertIn("[DEBUG] trace", stream.getvalue())

    def test_info_output(self):
        logger, stream = self._make_stream_logger(
            logger_name="test_info", level=logging.DEBUG
        )
        logger.info("running")
        self.assertIn("[INFO] running", stream.getvalue())

    def test_warning_output(self):
        logger, stream = self._make_stream_logger(
            logger_name="test_warn", level=logging.DEBUG
        )
        logger.warning("caution")
        self.assertIn("[WARNING] caution", stream.getvalue())

    def test_error_output(self):
        logger, stream = self._make_stream_logger(
            logger_name="test_err", level=logging.DEBUG
        )
        logger.error("fail")
        self.assertIn("[ERROR] fail", stream.getvalue())

    def test_critical_output(self):
        logger, stream = self._make_stream_logger(
            logger_name="test_crit", level=logging.DEBUG
        )
        logger.critical("boom")
        self.assertIn("[CRITICAL] boom", stream.getvalue())

    def test_respects_level_filtering(self):
        logger, stream = self._make_stream_logger(
            logger_name="test_filter", level=logging.WARNING
        )
        logger.info("should not appear")
        logger.warning("should appear")
        value = stream.getvalue()
        self.assertNotIn("should not appear", value)
        self.assertIn("should appear", value)


class GetLoggerTests(unittest.TestCase):
    def test_get_logger_returns_logger(self):
        logger = get_logger("test_gl", use_color=False)
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(logger.name, "test_gl")

    def test_get_logger_default_level(self):
        logger = get_logger("test_gl_default", use_color=False)
        self.assertEqual(logger.level, logging.NOTSET)


class EnvironmentVariableTests(unittest.TestCase):
    def setUp(self):
        self._saved = {}
        for var in (
            "COLOURED_LOGGER_COLOR",
            "FLASK_LOG_COLOR",
            "COLOURED_LOGGER_DATE_FORMAT",
            "FLASK_LOG_DATE_FORMAT",
        ):
            self._saved[var] = os.environ.pop(var, None)

    def tearDown(self):
        for var, value in self._saved.items():
            if value is not None:
                os.environ[var] = value
            elif var in os.environ:
                del os.environ[var]

    def test_colour_env_var_true(self):
        os.environ["COLOURED_LOGGER_COLOR"] = "true"
        formatter = ColouredFormatter()
        self.assertTrue(formatter.use_color)

    def test_colour_env_var_false(self):
        os.environ["COLOURED_LOGGER_COLOR"] = "false"
        formatter = ColouredFormatter()
        self.assertFalse(formatter.use_color)

    def test_flask_color_overrides_coloured_logger_color(self):
        os.environ["COLOURED_LOGGER_COLOR"] = "true"
        os.environ["FLASK_LOG_COLOR"] = "false"
        formatter = ColouredFormatter()
        self.assertFalse(formatter.use_color)

    def test_date_format_env_var(self):
        os.environ["COLOURED_LOGGER_DATE_FORMAT"] = "%H:%M"
        formatter = ColouredFormatter(use_color=False)
        self.assertEqual(formatter.datefmt, "%H:%M")

    def test_flask_date_format_overrides_coloured_date_format(self):
        os.environ["COLOURED_LOGGER_DATE_FORMAT"] = "%H:%M"
        os.environ["FLASK_LOG_DATE_FORMAT"] = "%Y"
        formatter = ColouredFormatter(use_color=False)
        self.assertEqual(formatter.datefmt, "%Y")


if __name__ == "__main__":
    unittest.main()
