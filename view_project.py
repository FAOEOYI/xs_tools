#!/usr/bin/env python3
import os
import sys
import re

def find_application_dir():
    """查找当前路径下的application目录"""
    current_dir = os.getcwd()
    application_dir = os.path.join(current_dir, 'application')
    
    if os.path.exists(application_dir) and os.path.isdir(application_dir):
        return application_dir
    else:
        print("错误: 未找到 'application' 目录!")
        sys.exit(1)

def find_samples_dir(application_dir):
    """查找application目录下的samples目录"""
    samples_dir = os.path.join(application_dir, 'samples')
    
    if os.path.exists(samples_dir) and os.path.isdir(samples_dir):
        return samples_dir
    else:
        print("错误: 未找到 'samples' 目录!")
        sys.exit(1)

def get_user_code_spaces(samples_dir):
    """获取所有用户代码空间"""
    user_code_spaces = []
    for item in os.listdir(samples_dir):
        item_path = os.path.join(samples_dir, item)
        if os.path.isdir(item_path):
            # 检查是否包含CMakeLists.txt或Kconfig文件
            if (os.path.exists(os.path.join(item_path, 'CMakeLists.txt')) or 
                os.path.exists(os.path.join(item_path, 'Kconfig'))):
                user_code_spaces.append(item)
    return user_code_spaces

def get_projects_in_user_space(samples_dir, user_space):
    """获取指定用户代码空间下的所有项目"""
    user_space_dir = os.path.join(samples_dir, user_space)
    
    if not os.path.exists(user_space_dir) or not os.path.isdir(user_space_dir):
        print(f"错误: 用户代码空间 '{user_space}' 不存在!")
        return []
    
    projects = []
    for item in os.listdir(user_space_dir):
        item_path = os.path.join(user_space_dir, item)
        if os.path.isdir(item_path):
            # 检查是否包含CMakeLists.txt或Kconfig文件
            if (os.path.exists(os.path.join(item_path, 'CMakeLists.txt')) or 
                os.path.exists(os.path.join(item_path, 'Kconfig'))):
                projects.append(item)
    return projects

def print_projects(projects, prefix=""):
    """打印项目列表"""
    if not projects:
        print(f"{prefix}未找到项目")
        return
    
    print(f"{prefix}找到 {len(projects)} 个项目:")
    for project in projects:
        print(f"{prefix}- {project}")

def main():
    # 查找application目录
    application_dir = find_application_dir()
    
    # 查找samples目录
    samples_dir = find_samples_dir(application_dir)
    
    # 处理命令行参数
    if len(sys.argv) == 1:
        print("用法: python View_project.py [all|<用户代码空间>]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "all":
        # 查找所有用户代码空间和项目
        user_code_spaces = get_user_code_spaces(samples_dir)
        
        if not user_code_spaces:
            print("未找到用户代码空间")
            sys.exit(0)
        
        print(f"找到 {len(user_code_spaces)} 个用户代码空间:")
        for user_space in user_code_spaces:
            print(f"- {user_space}")
            projects = get_projects_in_user_space(samples_dir, user_space)
            print_projects(projects, "  ")
    else:
        # 查找指定用户代码空间下的项目
        user_space = command
        projects = get_projects_in_user_space(samples_dir, user_space)
        print_projects(projects)

if __name__ == "__main__":
    main()    