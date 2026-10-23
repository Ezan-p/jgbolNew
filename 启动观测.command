#!/bin/zsh
cd "$(dirname "$0")" || exit 1
exec python3 observe_game.py collect --history
