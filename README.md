# coloured-logger

A lightweight Python package that adds coloured, standard `logging` output for Flask, FastAPI, or any Python app.

## Install

```bash
pip install coloured-logger
```

## Quick usage

```python
from coloured_logger import get_logger

logger = get_logger("my-app")
logger.info("Server started")
logger.success("Database connected")
logger.warning("High memory usage")
logger.error("Request failed")
```

## Flask example

```python
from flask import Flask
from coloured_logger import setup_logging

app = Flask(__name__)
setup_logging(logger_name="flask.app")
```

## FastAPI example

```python
from fastapi import FastAPI
from coloured_logger import setup_logging

app = FastAPI()
setup_logging(logger_name="uvicorn")
```

## Environment variables

- `FLASK_LOG_COLOR` or `COLOURED_LOGGER_COLOR`: enable/disable colors (`True` by default)
- `FLASK_LOG_DATE_FORMAT` or `COLOURED_LOGGER_DATE_FORMAT`: timestamp format

## Publishing workflow

Pushes to `main` trigger a GitHub Actions workflow that:
1. Creates an automatic version (`0.1.<run_number>`)
2. Builds the package
3. Publishes to PyPI

Configure a Trusted Publisher in PyPI for this repository/workflow to enable OIDC-based publishing (no API token required).
