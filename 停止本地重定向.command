#!/bin/zsh
set -e
cd "${0:A:h}"
.runtime/venv/bin/python redirect_game.py stop
