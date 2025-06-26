#!/usr/bin/env python3
import os
import sys
import stat
import re
import argparse
import shutil

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

def check_project_exists(project_name, user_project_dir):
    project_dir = os.path.join(user_project_dir, project_name.upper())
    return os.path.exists(project_dir) and os.path.isdir(project_dir)

def remove_from_cmakelists(project_name, user_project_dir):
    cmake_file = os.path.join(user_project_dir, 'CMakeLists.txt')
    
    if not os.path.exists(cmake_file):
        print(f"错误: {cmake_file} 文件不存在!")
        return False
    
    with open(cmake_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 构建要删除的内容
    entry_to_remove = f'''
if(DEFINED CONFIG_SAMPLE_SUPPORT_{project_name.upper()})
  add_subdirectory_if_exist({project_name.upper()})
endif()
'''
    
    if entry_to_remove not in content:
        print(f"警告: 在 {cmake_file} 中未找到项目相关配置!")
        return True
    
    # 移除相关内容
    updated_content = content.replace(entry_to_remove, '')
    
    with open(cmake_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"已从 {cmake_file} 中移除项目配置")
    return True

def remove_from_kconfig(project_name, user_project_dir):
    kconfig_file = os.path.join(user_project_dir, 'Kconfig')
    
    if not os.path.exists(kconfig_file):
        print(f"错误: {kconfig_file} 文件不存在!")
        return False
    
    with open(kconfig_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 构建要删除的内容
    config_entry = f'''
config SAMPLE_SUPPORT_{project_name.upper()}
  bool
  prompt "Support {project_name.upper()} Sample."
  default n
  depends on ENABLE_{user_project_dir.split('/')[-1].upper()}_SAMPLE
  help
    This option means support {project_name.upper()} Sample.

if SAMPLE_SUPPORT_{project_name.upper()}

menu "{project_name.upper()} Sample Configuration"
  osource "application/samples/{user_project_dir.split('/')[-1]}/{project_name.upper()}/Kconfig"
endmenu

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

def remove_project_dir(project_name, user_project_dir):
    project_dir = os.path.join(user_project_dir, project_name.upper())
    
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
    parser = argparse.ArgumentParser(description='删除项目工具')
    parser.add_argument('project_name', help='项目名称')
    parser.add_argument('-p', '--parent', help='指定父级用户代码空间名称')
    
    args = parser.parse_args()
    
    project_name = args.project_name
    parent_space = args.parent
    
    # 验证项目名是否符合变量名规则
    if not is_valid_project_name(project_name):
        sys.exit(1)
    
    print(f"开始删除项目 '{project_name}'...")
    
    # 查找application目录
    application_dir = find_application_dir()
    
    # 定位user_project目录
    if parent_space:
        user_project_dir = os.path.join(application_dir, 'samples', parent_space)
    else:
        user_project_dir = os.path.join(application_dir, 'samples', 'user_project')
    
    if not os.path.exists(user_project_dir):
        print(f"错误: {user_project_dir} 目录不存在!")
        sys.exit(1)
    
    # 检查项目是否存在
    if not check_project_exists(project_name, user_project_dir):
        print(f"错误: 项目 '{project_name}' 不存在!")
        sys.exit(1)
    
    # 确认用户是否真的要删除
    confirmation = input(f"确定要删除项目 '{project_name}' 吗？这将删除所有相关文件。(y/N): ")
    if confirmation.lower() != 'y':
        print("操作已取消")
        sys.exit(0)
    
    # 1. 从Kconfig中移除项目配置
    if not remove_from_kconfig(project_name, user_project_dir):
        print("删除过程中出现错误，项目可能未被完全删除!")
        sys.exit(1)
    
    # 2. 从CMakeLists.txt中移除项目配置
    if not remove_from_cmakelists(project_name, user_project_dir):
        print("删除过程中出现错误，项目可能未被完全删除!")
        sys.exit(1)
    
    # 3. 删除项目目录
    if not remove_project_dir(project_name, user_project_dir):
        print("删除过程中出现错误，项目目录可能未被完全删除!")
        sys.exit(1)
    
    print(f"\n项目 '{project_name}' 已成功删除!")

if __name__ == "__main__":
    main()    