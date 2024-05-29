#!/usr/bin/env bash

# Directory of the script
SCRIPT_DIR="$(cd -- $(dirname -- "$0") && pwd)"

DIR="$(PWD)"

if [ -d "$SCRIPT_DIR/venv" ]; then
    source "$SCRIPT_DIR/venv/bin/activate" || exit 1
else
    echo "venv folder does not exist. Not activating..."
fi

# 拷贝common.yaml
if [ ! -f "$SCRIPT_DIR/config/common.yaml" ]; then
    cp "$SCRIPT_DIR/config/common.example.yaml" "$SCRIPT_DIR/config/common.yaml"
    echo "common.yaml 不存在,自动拷贝"
fi

python open_all.py
