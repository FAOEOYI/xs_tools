#!/bin/bash

# 创建tools目录（如果不存在）
TOOLS_DIR="$PWD/tools"
mkdir -p "$TOOLS_DIR"

# 检查tools目录是否有xs文件，如果没有则给出提示
XS_SCRIPT="$TOOLS_DIR/xs"
if [ ! -f "$XS_SCRIPT" ]; then
    echo "警告：$XS_SCRIPT 文件不存在，请确保该文件已正确创建并具有可执行权限。"
else
    # 将tools目录添加到PATH环境变量中
    export PATH="$TOOLS_DIR:$PATH"

    # 验证xs命令是否可用
    if command -v xs &> /dev/null; then
        echo "已成功将 '$TOOLS_DIR' 目录添加到 PATH 环境变量中。"
        echo "现在你可以在当前终端会话中直接使用 'xs' 命令。"
        echo "以下是 'xs' 命令可执行的相关操作："
        echo "1. 用户代码空间创建与删除："
        echo "   - 创建默认用户代码空间: xs make-user-space"
        echo "   - 创建指定用户代码空间: xs make-user-space <用户代码空间名>"
        echo "   - 删除指定用户代码空间: xs clean-user-space <用户代码空间名>"
        echo "   - 强制删除指定用户代码空间: xs clean-user-space <用户代码空间名> -f"
        echo "2. 项目创建与删除："
        echo "   - 创建默认代码空间的示例项目: xs create-project <项目名>"
        echo "   - 创建指定代码空间的示例项目: xs create-project <项目名> -p <用户代码空间名>"
        echo "   - 删除默认代码空间的示例项目: xs clean-project <项目名>"
        echo "   - 删除指定代码空间的示例项目: xs clean-project <项目名> -p <用户代码空间名>"
        echo "3. 编译与配置："
        echo "   - 可选择式增量编译: xs b"
        echo "   - 可选择式全量编译: xs b -c"
        echo "   - 启动 ws63 - liteos - app 目标的增量编译: xs build"
        echo "   - 启动 ws63 - liteos - app 目标的全量编译: xs build -c"
        echo "   - 可选择式启动目标的 menuconfig 图形配置界面: xs menu"
        echo "   - 启动 ws63 - liteos - app 目标的 menuconfig 图形配置界面: xs menuconfig"
        echo "4. 项目查找："
        echo "   - 查找所有项目: xs find all"
        echo "   - 查找指定代码空间的项目: xs find <代码空间>"
    else
        echo "错误：无法找到 'xs' 命令，请检查 $TOOLS_DIR 目录权限或确保 'xs' 文件存在且可执行。"
    fi
fi

echo "窗口关闭后，'xs' 命令将自动失效。若要长期使用，可将 'export PATH=$TOOLS_DIR:\$PATH' 添加到你的 shell 配置文件（如 ~/.bashrc 或 ~/.zshrc）中。"