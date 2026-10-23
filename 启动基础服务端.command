#!/bin/zsh
set -e
cd "${0:A:h}"
exec python3 game_server.py --probe
