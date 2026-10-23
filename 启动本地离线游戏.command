#!/bin/zsh
set -e
cd "${0:A:h}"
python3 start_game.py
.runtime/venv/bin/python redirect_game.py stop
.runtime/venv/bin/python redirect_game.py start --offline --probe
.runtime/venv/bin/python redirect_game.py status
