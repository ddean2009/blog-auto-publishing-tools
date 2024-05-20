#!/usr/bin/env bash

# Directory of the script
SCRIPT_DIR="$(cd -- $(dirname -- "$0") && pwd)"

DIR="$(PWD)"

if [ -d "$SCRIPT_DIR/venv" ]; then
    source "$SCRIPT_DIR/venv/bin/activate" || exit 1
else
    echo "venv folder does not exist. Not activating..."
fi

#Set STARTUP_CMD as normal python if not specified
if [[ -z "$STARTUP_CMD" ]]
then
    STARTUP_CMD=python
fi

python publish_all.py
