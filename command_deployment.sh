#!/bin/bash

#将set_xs.sh放在上一级目录
cp ./set_xs.sh ../

#将 xs 放在上一级目录的tools目录下
cp ./xs ../tools/

echo "部署完成"
echo "请在src目录手动执行set_xs.sh" 