#!/bin/zsh
cd -- "${0:A:h}" || exit 1
if ! /usr/bin/python3 redirect_game.py stop; then
  read -r "?重定向尚未停止，按回车关闭窗口。"
  exit 1
fi
/usr/bin/python3 android_emulator/run.py --config game.json stop
result=$?
if (( result != 0 )); then
  read -r "?停止失败，按回车关闭窗口。"
fi
exit $result
