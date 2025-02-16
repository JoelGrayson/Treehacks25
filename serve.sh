#!/bin/bash
set -e

uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 6969