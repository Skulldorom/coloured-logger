# python-coloured-logger

A lightweight Python package that provides clean, coloured logging output for Flask, FastAPI, and any standard Python application.

It extends Python’s built-in `logging` module with readable coloured console output and simple setup helpers.

---

## Features

- Coloured console logging
- Works with standard Python `logging`
- Flask integration
- FastAPI / Uvicorn integration
- Simple setup API
- Lightweight with minimal configuration

---

## Installation

Install from PyPI:

```bash
pip install python-coloured-logger
```

---

## Quick Start

```python
from coloured_logger import get_logger

logger = get_logger("my-app")

logger.debug("Debug message")
logger.info("Server started")
logger.success("Database connected")
logger.warning("High memory usage")
logger.error("Request failed")
logger.critical("System crash")
```

Example output:

```text
[2026-05-27 12:00:00] INFO     Server started
[2026-05-27 12:00:01] SUCCESS  Database connected
[2026-05-27 12:00:02] WARNING  High memory usage
[2026-05-27 12:00:03] ERROR    Request failed
```

---

## Flask Integration

```python
from flask import Flask
from coloured_logger import setup_logging

app = Flask(__name__)

setup_logging(logger_name="flask.app")

@app.route("/")
def index():
    app.logger.info("Request received")
    return "Hello World"
```

---

## FastAPI Integration

```python
from fastapi import FastAPI
from coloured_logger import setup_logging

app = FastAPI()

setup_logging(logger_name="uvicorn")

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

---

## Standard Python Logging

```python
from coloured_logger import setup_logging
import logging

setup_logging()

logger = logging.getLogger("example")

logger.info("Using standard logging")
```

---

## Environment Variables

### Enable or Disable Colours

By default, colours are enabled.

```bash
COLOURED_LOGGER_COLOR=True
```

or for Flask-specific configuration:

```bash
FLASK_LOG_COLOR=True
```

Disable colours:

```bash
COLOURED_LOGGER_COLOR=False
```

---

### Custom Date Format

```bash
COLOURED_LOGGER_DATE_FORMAT=%Y-%m-%d %H:%M:%S
```

or:

```bash
FLASK_LOG_DATE_FORMAT=%H:%M:%S
```

---

## Supported Log Levels

| Level | Description |
|---|---|
| `debug` | Debug information |
| `info` | General information |
| `success` | Successful operations |
| `warning` | Warning messages |
| `error` | Error messages |
| `critical` | Critical failures |

---


## Requirements

- Python 3.9+
- Flask (optional)
- FastAPI / Uvicorn (optional)

---

## License

MIT License

---

## Contributing

Pull requests, issues, and suggestions are welcome.

If you find a bug or want to improve the package, feel free to open an issue or submit a PR.

---

## Links

- PyPI: `https://pypi.org/project/python-coloured-logger/`
- GitHub: `https://github.com/Skulldorom/python-coloured-logger`
