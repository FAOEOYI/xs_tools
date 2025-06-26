#!/bin/bash

# 获取上一级目录路径
PARENT_DIR="./xs_tools/"

BUILD_DIR="./"

case "$1" in
    -h)
        echo "====================================================================="
        echo "xs 命令索引"
        echo "====================================================================="
        echo "xs -h                                         【帮助】"
        echo "xs --help                                     【详细帮助】"
        echo "xs b                                          【可选择式增量编译指令】"
        echo "xs b -c                                       【可选择式全量编译指令】"
        echo "xs menu                                       【可选择式启动目标的menuconfig图形配置界面】"
        echo "xs build                                      【启动 ws63-liteos-app 目标的增量编译指令】"
        echo "xs build -c                                   【启动 ws63-liteos-app 目标的全量编译指令】"
        echo "xs menuconfig                                 【启动 ws63-liteos-app 目标的menuconfig图形配置界面】"
        echo "xs make-user-space                            【创建默认用户代码空间】"
        echo "xs make-user-space <用户代码空间名>           【创建自定义名称用户代码空间】"
        echo "xs create-project <项目名>                    【在默认用户代码空间创建项目】"
        echo "xs create-project <项目名> -p <用户代码空间名>【在指定用户代码空间创建项目】"
        echo "xs clean-user-space <用户代码空间名>          【删除指定用户代码空间】"
        echo "xs clean-user-space <用户代码空间名> -f       【强制删除指定用户代码空间】"
        echo "xs clean-project <项目名>                     【删除默认用户代码空间的项目】"
        echo "xs clean-project <项目名> -p <用户代码空间名> 【删除指定用户代码空间的项目】"
        echo "xs find all                                   【查找所有项目】"
        echo "xs find <代码空间>                            【查找指定代码空间的项目】"
        echo "====================================================================="
        ;;
    --help)
        echo "====================================================================="
        echo " xs 命令帮助文档"
        echo "====================================================================="
        echo "xs 是一个便捷的命令行工具，用于简化开发过程中的常见操作，如用户代码空间管理、项目创建与删除、编译和配置等。"
        echo ""
        echo "使用方法:"
        echo "  xs [子命令] [选项]"
        echo ""
        echo "子命令列表:"
        echo "  make-user-space    创建用户代码空间"
        echo "  create-project     创建项目"
        echo "  clean-user-space   删除用户代码空间"
        echo "  clean-project      删除项目"
        echo "  b                  可选择式编译"
        echo "  build              启动 ws63-liteos-app 目标编译"
        echo "  menu               可选择式启动目标的 menuconfig 图形配置界面"
        echo "  menuconfig         启动 ws63-liteos-app 目标的 menuconfig 图形配置界面"
        echo "  -h                 显示简要帮助信息"
        echo "  --help             显示此详细帮助信息"
        echo ""
        echo "子命令详细说明及示例:"
        echo ""
        echo "### 用户代码空间管理"
        echo "#### 创建默认用户代码空间"
        echo "  描述: 创建名为 user_project 的默认用户代码空间。"
        echo "  命令: xs make-user-space"
        echo "  示例: xs make-user-space"
        echo ""
        echo "#### 创建自定义名称用户代码空间"
        echo "  描述: 创建一个指定名称的用户代码空间。"
        echo "  命令: xs make-user-space <用户代码空间名>"
        echo "  示例: xs make-user-space TEST001"
        echo ""
        echo "#### 删除指定用户代码空间"
        echo "  描述: 删除指定名称的用户代码空间。"
        echo "  命令: xs clean-user-space <用户代码空间名>"
        echo "  示例: xs clean-user-space TEST001"
        echo ""
        echo "#### 强制删除指定用户代码空间"
        echo "  描述: 强制删除指定名称的用户代码空间，忽略可能的错误提示。"
        echo "  命令: xs clean-user-space <用户代码空间名> -f"
        echo "  示例: xs clean-user-space TEST001 -f"
        echo ""
        echo "### 项目管理"
        echo "#### 在默认用户代码空间创建项目"
        echo "  描述: 在默认的 user_project 代码空间中创建一个项目。"
        echo "  命令: xs create-project <项目名>"
        echo "  示例: xs create-project T_001"
        echo ""
        echo "#### 在指定用户代码空间创建项目"
        echo "  描述: 在指定名称的用户代码空间中创建一个项目。"
        echo "  命令: xs create-project <项目名> -p <用户代码空间名>"
        echo "  示例: xs create-project T_001 -p TEST001"
        echo ""
        echo "#### 删除默认用户代码空间的项目"
        echo "  描述: 删除默认的 user_project 代码空间中的指定项目。"
        echo "  命令: xs clean-project <项目名>"
        echo "  示例: xs clean-project T_001"
        echo ""
        echo "#### 删除指定用户代码空间的项目"
        echo "  描述: 删除指定名称的用户代码空间中的指定项目。"
        echo "  命令: xs clean-project <项目名> -p <用户代码空间名>"
        echo "  示例: xs clean-project T_001 -p TEST001"
        echo ""
        echo "### 编译与配置"
        echo "#### 可选择式增量编译"
        echo "  描述: 进行可选择式的增量编译。"
        echo "  命令: xs b"
        echo "  示例: xs b"
        echo ""
        echo "#### 可选择式全量编译"
        echo "  描述: 进行可选择式的全量编译。"
        echo "  命令: xs b -c"
        echo "  示例: xs b -c"
        echo ""
        echo "#### 启动 ws63-liteos-app 目标的增量编译"
        echo "  描述: 启动 ws63-liteos-app 目标的增量编译。"
        echo "  命令: xs build"
        echo "  示例: xs build"
        echo ""
        echo "#### 启动 ws63-liteos-app 目标的全量编译"
        echo "  描述: 启动 ws63-liteos-app 目标的全量编译。"
        echo "  命令: xs build -c"
        echo "  示例: xs build -c"
        echo ""
        echo "#### 可选择式启动目标的 menuconfig 图形配置界面"
        echo "  描述: 启动可选择式目标的 menuconfig 图形配置界面。"
        echo "  命令: xs menu"
        echo "  示例: xs menu"
        echo ""
        echo "#### 启动 ws63-liteos-app 目标的 menuconfig 图形配置界面"
        echo "  描述: 启动 ws63-liteos-app 目标的 menuconfig 图形配置界面。"
        echo "  命令: xs menuconfig"
        echo "  示例: xs menuconfig"
        echo ""
        echo "### 项目查找"
        echo "#### 查找所有项目"
        echo "  描述: 查找所有存在的项目。"
        echo "  命令: xs find all"
        echo "  示例: xs find all"
        echo ""
        echo "#### 查找指定代码空间的项目"
        echo "  描述: 查找指定代码空间中的项目。"
        echo "  命令: xs find <代码空间>"
        echo "  示例: xs find TEST001"
        echo ""
        echo "====================================================================="
        ;;
    b)
        if [ -z "$2" ]; then
            python ${BUILD_DIR}build.py
        elif [ "$2" = "-c" ]; then
            python ${BUILD_DIR}build.py -c
        fi
        ;;
    menu)
        python ${BUILD_DIR}build.py menuconfig
        ;;
    build)
        if [ -z "$2" ]; then
            python ${BUILD_DIR}build.py ws63-liteos-app
        elif [ "$2" = "-c" ]; then
            python ${BUILD_DIR}build.py -c ws63-liteos-app
        fi
        ;;
    menuconfig)
        python ${BUILD_DIR}build.py ws63-liteos-app menuconfig
        ;;
    make-user-space)
        if [ -z "$2" ]; then
            python ${PARENT_DIR}mucs.py
        else
            python ${PARENT_DIR}mucs.py "$2"
        fi
        ;;
    create-project)
        if [ -n "$2" ] && [ -z "$3" ]; then
            python ${PARENT_DIR}mkpro.py "$2"
        elif [ -n "$2" ] && [ "$3" = "-p" ] && [ -n "$4" ]; then
            python ${PARENT_DIR}mkpro.py "$2" -p "$4"
        fi
        ;;
    clean-user-space)
        if [ -n "$2" ] && [ -z "$3" ]; then
            python ${PARENT_DIR}rmucs.py "$2"
        elif [ -n "$2" ] && [ "$3" = "-f" ]; then
            python ${PARENT_DIR}rmucs.py "$2" -f
        fi
        ;;
    clean-project)
        if [ -n "$2" ] && [ -z "$3" ]; then
            python ${PARENT_DIR}rmpro.py "$2"
        elif [ -n "$2" ] && [ "$3" = "-p" ] && [ -n "$4" ]; then
            python ${PARENT_DIR}rmpro.py "$2" -p "$4"
        fi
        ;;
    find)
        if [ "$2" = "all" ]; then
            python ${PARENT_DIR}view_project.py all
        elif [ -n "$2" ]; then
            python ${PARENT_DIR}view_project.py "$2"
        else
            echo "无效的参数，请使用 xs find all 查找所有项目，或使用 xs find <代码空间> 查找指定代码空间的项目。"
            exit 1
        fi
        ;;
    *)
        echo "无效的命令，请使用 xs -h 查看简要帮助信息，或使用 xs --help 查看详细帮助信息。"
        exit 1
        ;;
esac

