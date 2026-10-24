#!/bin/zsh
set -e
cd "${0:A:h}"
python3 start_game.py --client-only
.runtime/venv/bin/python redirect_game.py start --probe
.runtime/venv/bin/python redirect_game.py status
