#!/bin/zsh
cd -- "${0:A:h}" || exit 1
/usr/bin/python3 start_game.py --repair
result=$?
if (( result != 0 )); then
  read -r "?修复未完成，请保留报错信息。按回车关闭窗口。"
fi
exit $result
