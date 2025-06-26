#!/usr/bin/env python3
import os
import sys
import stat
import re

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

def create_user_project_dir(samples_dir, project_name):
    user_project_dir = os.path.join(samples_dir, project_name)
    
    if not os.path.exists(user_project_dir):
        os.makedirs(user_project_dir)
        print(f"已创建用户项目目录: {user_project_dir}")
    else:
        print(f"警告: 用户项目目录 {user_project_dir} 已存在!")
    
    return user_project_dir

def create_user_project_cmakelists(user_project_dir, project_name):
    cmake_file = os.path.join(user_project_dir, 'CMakeLists.txt')
    
    if os.path.exists(cmake_file):
        print(f"警告: {cmake_file} 已存在!")
        return
    
    cmake_content = f'''# User project CMakeLists.txt for {project_name}

# Example project configuration
# if(DEFINED CONFIG_SAMPLE_SUPPORT_TEST_PROJECT)
#     add_subdirectory_if_exist(TEST_PROJECT)
# endif()

set(SOURCES "${{SOURCES}}" PARENT_SCOPE)
set(PUBLIC_HEADER "${{PUBLIC_HEADER}}" PARENT_SCOPE)
'''
    
    with open(cmake_file, 'w', encoding='utf-8') as f:
        f.write(cmake_content)
    
    # 修改权限为777
    os.chmod(cmake_file, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    print(f"已创建并设置权限: {cmake_file}")

def create_user_project_kconfig(user_project_dir, project_name):
    kconfig_file = os.path.join(user_project_dir, 'Kconfig')
    
    if os.path.exists(kconfig_file):
        print(f"警告: {kconfig_file} 已存在!")
        return
    
    kconfig_content = f'''# User project Kconfig for {project_name}

# Example project configuration
# config SAMPLE_SUPPORT_TEST_PROJECT
#     bool
#     prompt "Support test_project Sample."
#     default n
#     depends on ENABLE_{project_name.upper()}_SAMPLE
#     help
#         This option means support test_project Sample.

# if SAMPLE_SUPPORT_TEST_PROJECT
# menu "TEST_PROJECT Sample Configuration"
#     osource "application/samples/{project_name}/TEST_PROJECT/Kconfig"
# endmenu
# endif
'''
    
    with open(kconfig_file, 'w', encoding='utf-8') as f:
        f.write(kconfig_content)
    
    # 修改权限为777
    os.chmod(kconfig_file, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    print(f"已创建并设置权限: {kconfig_file}")

def update_samples_kconfig(samples_dir, project_name):
    kconfig_file = os.path.join(samples_dir, 'Kconfig')
    
    # 检查文件是否存在
    if not os.path.exists(kconfig_file):
        print(f"错误: {kconfig_file} 文件不存在!")
        sys.exit(1)
    
    # 读取文件内容
    with open(kconfig_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已添加过配置
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
    
    if config_entry in content:
        print(f"警告: {kconfig_file} 中已存在 {project_name} 配置!")
        return
    
    # 添加配置到文件末尾
    with open(kconfig_file, 'a', encoding='utf-8') as f:
        f.write(config_entry)
    
    print(f"已更新 {kconfig_file}")

def update_samples_cmakelists(samples_dir, project_name):
    cmake_file = os.path.join(samples_dir, 'CMakeLists.txt')
    
    # 检查文件是否存在
    if not os.path.exists(cmake_file):
        print(f"错误: {cmake_file} 文件不存在!")
        sys.exit(1)
    
    # 读取文件内容
    with open(cmake_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 添加 add_subdirectory 语句
    subdir_entry = f'''
if(DEFINED CONFIG_ENABLE_{project_name.upper()}_SAMPLE)
    add_subdirectory_if_exist({project_name})
endif()
'''
    
    if subdir_entry not in content:
        # 找到custom的位置
        custom_pos = content.find('add_subdirectory_if_exist(custom)')
        if custom_pos == -1:
            # 如果找不到custom，就添加到所有if语句后面
            insert_pos = content.find('add_subdirectory_if_exist(custom)')
            if insert_pos == -1:
                # 如果连custom都没有，就添加到最后一个endif后面
                endif_pos = content.rfind('endif()')
                if endif_pos != -1:
                    insert_pos = endif_pos + 7  # endif()的长度
                else:
                    # 如果没有endif，就添加到文件末尾
                    insert_pos = len(content)
            else:
                insert_pos = custom_pos
        else:
            insert_pos = custom_pos
        
        content = content[:insert_pos] + subdir_entry + content[insert_pos:]
    else:
        print(f"警告: {cmake_file} 中已存在 {project_name} 的 add_subdirectory 配置!")
    
    # 添加 install_sdk 语句
    install_entry = f'install_sdk("${{CMAKE_CURRENT_SOURCE_DIR}}/{project_name}" "*")\n'
    
    if install_entry not in content:
        # 找到build_component()的位置
        build_pos = content.find('build_component()')
        if build_pos == -1:
            # 如果找不到build_component，就添加到文件末尾
            content += install_entry
        else:
            # 在build_component之前添加
            content = content[:build_pos] + install_entry + content[build_pos:]
    else:
        print(f"警告: {cmake_file} 中已存在 {project_name} 的 install_sdk 配置!")
    
    # 写入更新后的内容
    with open(cmake_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已更新 {cmake_file}")

def main():
    # 不输入参数时，默认创建user_project用户代码空间
    if len(sys.argv) == 1:
        project_name = "user_project"
        print("未指定项目名，默认创建 'user_project' 用户代码空间")
    elif len(sys.argv) == 2:
        project_name = sys.argv[1]
    else:
        print(f"用法: {sys.argv[0]} [项目名]")
        print("若不指定项目名，将默认创建 'user_project' 用户代码空间")
        sys.exit(1)
    
    # 验证项目名是否符合变量名规则
    if not is_valid_project_name(project_name):
        sys.exit(1)
    
    print(f"开始创建用户代码空间 '{project_name}'...")
    
    # 查找application目录
    application_dir = find_application_dir()
    
    # 定位samples目录
    samples_dir = os.path.join(application_dir, 'samples')
    
    if not os.path.exists(samples_dir):
        print(f"错误: {samples_dir} 目录不存在!")
        sys.exit(1)
    
    # 2. 创建用户项目目录
    user_project_dir = create_user_project_dir(samples_dir, project_name)
    
    # 3. 创建用户项目CMakeLists.txt
    create_user_project_cmakelists(user_project_dir, project_name)
    
    # 4. 创建用户项目Kconfig
    create_user_project_kconfig(user_project_dir, project_name)
    
    # 5. 更新samples目录下的Kconfig文件
    update_samples_kconfig(samples_dir, project_name)
    
    # 6. 更新samples目录下的CMakeLists.txt文件
    update_samples_cmakelists(samples_dir, project_name)
    
    print(f"\n用户代码空间 '{project_name}' 创建完成!")
    print(f"接下来可以使用 mkpro.py 脚本在 {project_name} 下创建具体项目")

if __name__ == "__main__":
    main()        