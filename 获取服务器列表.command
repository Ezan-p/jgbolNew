#!/bin/zsh
cd "${0:A:h}" || exit 1
.runtime/venv/bin/python fetch_server_list.py || exit 1
open analysis/server_lists/服务器列表.txt
