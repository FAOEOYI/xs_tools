#!/usr/bin/env python3
import os
import sys
import stat
import re
import shutil
import argparse

def is_valid_project_name(name):
    # 检查是否是有效的变量名
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name):
        print(f"错误: 项目名 '{name}' 不符合变量名规则")
        print("项目名必须以字母或下划线开头，后面可以跟字母、数字或下划线")
        return False
    return True

def find_application_dir():
    current_dir = os.getcwd()
    application_dir = os.path.join(current_dir, 'application')
    
    if os.path.exists(application_dir) and os.path.isdir(application_dir):
        return application_dir
    else:
        print("错误: 未找到 'application' 目录!")
        sys.exit(1)

def check_project_exists(samples_dir, project_name):
    project_dir = os.path.join(samples_dir, project_name)
    return os.path.exists(project_dir) and os.path.isdir(project_dir)

def check_sub_projects(samples_dir, project_name):
    """检查用户代码空间下是否存在项目目录"""
    user_project_dir = os.path.join(samples_dir, project_name)
    if not os.path.exists(user_project_dir):
        return []
    
    # 查找所有包含Kconfig或CMakeLists.txt的子目录
    sub_projects = []
    for item in os.listdir(user_project_dir):
        item_path = os.path.join(user_project_dir, item)
        if os.path.isdir(item_path):
            if (os.path.exists(os.path.join(item_path, 'Kconfig')) or
                os.path.exists(os.path.join(item_path, 'CMakeLists.txt'))):
                sub_projects.append(item)
    
    return sub_projects

def remove_from_kconfig(samples_dir, project_name):
    kconfig_file = os.path.join(samples_dir, 'Kconfig')
    
    if not os.path.exists(kconfig_file):
        print(f"错误: {kconfig_file} 文件不存在!")
        return False
    
    with open(kconfig_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 构建要删除的内容
    config_entry = f'''
config ENABLE_{project_name.upper()}_SAMPLE
    bool
    prompt "Enable the Sample of {project_name}."
    default n
    depends on SAMPLE_ENABLE
    help
        This option means enable the sample of {project_name}.

if ENABLE_{project_name.upper()}_SAMPLE
osource "application/samples/{project_name}/Kconfig"
endif
'''
    
    if config_entry not in content:
        print(f"警告: 在 {kconfig_file} 中未找到项目相关配置!")
        return True
    
    # 移除相关内容
    updated_content = content.replace(config_entry, '')
    
    with open(kconfig_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"已从 {kconfig_file} 中移除项目配置")
    return True

def remove_from_cmakelists(samples_dir, project_name):
    cmake_file = os.path.join(samples_dir, 'CMakeLists.txt')
    
    if not os.path.exists(cmake_file):
        print(f"错误: {cmake_file} 文件不存在!")
        return False
    
    with open(cmake_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 移除 add_subdirectory 语句
    subdir_entry = f'''
if(DEFINED CONFIG_ENABLE_{project_name.upper()}_SAMPLE)
    add_subdirectory_if_exist({project_name})
endif()
'''
    
    if subdir_entry in content:
        content = content.replace(subdir_entry, '')
        print(f"已从 {cmake_file} 中移除项目的 add_subdirectory 配置")
    else:
        print(f"警告: 在 {cmake_file} 中未找到项目的 add_subdirectory 配置!")
    
    # 移除 install_sdk 语句
    install_entry = f'install_sdk("${{CMAKE_CURRENT_SOURCE_DIR}}/{project_name}" "*")\n'
    
    if install_entry in content:
        content = content.replace(install_entry, '')
        print(f"已从 {cmake_file} 中移除项目的 install_sdk 配置")
    else:
        print(f"警告: 在 {cmake_file} 中未找到项目的 install_sdk 配置!")
    
    # 写入更新后的内容
    with open(cmake_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def remove_project_dir(samples_dir, project_name):
    project_dir = os.path.join(samples_dir, project_name)
    
    if not os.path.exists(project_dir):
        print(f"错误: 项目目录 {project_dir} 不存在!")
        return False
    
    try:
        # 删除项目目录及其所有内容
        shutil.rmtree(project_dir)
        print(f"已删除项目目录: {project_dir}")
        return True
    except Exception as e:
        print(f"错误: 删除项目目录失败: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='删除用户代码空间工具')
    parser.add_argument('project_name', help='用户代码空间名称')
    parser.add_argument('-f', '--force', action='store_true', help='强制删除，不提示确认')
    
    args = parser.parse_args()
    
    project_name = args.project_name
    force = args.force
    
    # 验证项目名是否符合变量名规则
    if not is_valid_project_name(project_name):
        sys.exit(1)
    
    print(f"开始删除用户代码空间 '{project_name}'...")
    
    # 查找application目录
    application_dir = find_application_dir()
    
    # 定位samples目录
    samples_dir = os.path.join(application_dir, 'samples')
    
    if not os.path.exists(samples_dir):
        print(f"错误: {samples_dir} 目录不存在!")
        sys.exit(1)
    
    # 检查项目是否存在
    if not check_project_exists(samples_dir, project_name):
        print(f"错误: 用户代码空间 '{project_name}' 不存在!")
        sys.exit(1)
    
    # 检查用户代码空间下是否有项目
    sub_projects = check_sub_projects(samples_dir, project_name)
    if sub_projects:
        print(f"错误: 用户代码空间 '{project_name}' 下存在项目: {', '.join(sub_projects)}")
        print("请先删除这些项目，或使用 -f 参数强制删除。")
        if not force:
            sys.exit(1)
        else:
            print("警告: 强制删除将删除用户代码空间及其所有子项目!")
    
    # 确认用户是否真的要删除
    if not force:
        confirmation = input(f"确定要删除用户代码空间 '{project_name}' 吗？这将删除所有相关文件。(y/N): ")
        if confirmation.lower() != 'y':
            print("操作已取消")
            sys.exit(0)
    
    # 1. 从Kconfig中移除项目配置
    if not remove_from_kconfig(samples_dir, project_name):
        print("删除过程中出现错误，项目可能未被完全删除!")
        sys.exit(1)
    
    # 2. 从CMakeLists.txt中移除项目配置
    if not remove_from_cmakelists(samples_dir, project_name):
        print("删除过程中出现错误，项目可能未被完全删除!")
        sys.exit(1)
    
    # 3. 删除项目目录
    if not remove_project_dir(samples_dir, project_name):
        print("删除过程中出现错误，项目目录可能未被完全删除!")
        sys.exit(1)
    
    print(f"\n用户代码空间 '{project_name}' 已成功删除!")

if __name__ == "__main__":
    main()        