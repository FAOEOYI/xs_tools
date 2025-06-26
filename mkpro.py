#!/usr/bin/env python3
import os
import sys
import stat
import re
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

def check_project_exists(project_name, user_project_dir):
    project_dir = os.path.join(user_project_dir, project_name.upper())
    if os.path.exists(project_dir) and os.path.isdir(project_dir):
        print(f"错误: 项目 '{project_name}' 已存在!")
        return True
    return False

def update_cmakelists(project_name, user_project_dir):
    cmake_file = os.path.join(user_project_dir, 'CMakeLists.txt')
    
    if not os.path.exists(cmake_file):
        print(f"错误: {cmake_file} 文件不存在!")
        sys.exit(1)
    
    with open(cmake_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    insert_pos = content.find('set(SOURCES "${SOURCES}" PARENT_SCOPE)')
    if insert_pos == -1:
        print("错误: 未找到插入位置!")
        sys.exit(1)
    
    new_entry = f'''
if(DEFINED CONFIG_SAMPLE_SUPPORT_{project_name.upper()})
  add_subdirectory_if_exist({project_name.upper()})
endif()
'''
    updated_content = content[:insert_pos] + new_entry + content[insert_pos:]
    
    with open(cmake_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"已更新 {cmake_file}")

def update_kconfig(project_name, user_project_dir):
    kconfig_file = os.path.join(user_project_dir, 'Kconfig')
    
    if not os.path.exists(kconfig_file):
        print(f"错误: {kconfig_file} 文件不存在!")
        sys.exit(1)
    
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
    
    with open(kconfig_file, 'a', encoding='utf-8') as f:
        f.write(config_entry)
    
    print(f"已更新 {kconfig_file}")

def create_project_dir(project_name, user_project_dir):
    project_dir = os.path.join(user_project_dir, project_name.upper())
    
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)
        print(f"已创建项目目录: {project_dir}")
    else:
        print(f"警告: 项目目录 {project_dir} 已存在!")
    
    return project_dir

def create_project_kconfig(project_name, project_dir):
    kconfig_path = os.path.join(project_dir, 'Kconfig')
    
    if os.path.exists(kconfig_path):
        print(f"警告: {kconfig_path} 已存在!")
        return
    
    with open(kconfig_path, 'w', encoding='utf-8') as f:
        f.write(f'''config {project_name.upper()}
    int
    prompt "{project_name.upper()}"
    default 0
''')
    
    # 修改权限为777
    os.chmod(kconfig_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    print(f"已创建并设置权限: {kconfig_path}")

def create_cmakelists(project_name, project_dir):
    cmake_path = os.path.join(project_dir, 'CMakeLists.txt')
    
    if os.path.exists(cmake_path):
        print(f"警告: {cmake_path} 已存在!")
        return
    
    with open(cmake_path, 'w', encoding='utf-8') as f:
        f.write(f'''set(PUBLIC_HEADER "${{PUBLIC_HEADER}}"  
"${{CMAKE_CURRENT_SOURCE_DIR}}/inc" 
PARENT_SCOPE)

set(SOURCES "${{SOURCES}}" 
"${{CMAKE_CURRENT_SOURCE_DIR}}/{project_name.upper()}.c" 
PARENT_SCOPE)
''')
    
    # 修改权限为777
    os.chmod(cmake_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    print(f"已创建并设置权限: {cmake_path}")

def create_c_file(project_name, project_dir):
    c_file_path = os.path.join(project_dir, f'{project_name.upper()}.c')
    
    if os.path.exists(c_file_path):
        print(f"警告: {c_file_path} 已存在!")
        return
    
    c_content = f'''#include "app_init.h"
#include "soc_osal.h"
#include "common_def.h"
#include "cmsis_os2.h"

#define {project_name.upper()}_TASK_STACK_SIZE    0x1000
#define {project_name.upper()}_TASK_PRIO          (osPriority_t)(17)
#define {project_name.upper()}_DURATION_MS        1000

static void *{project_name.lower()}_test_task(const char *arg)
{{
    unused(arg);

    while (1) {{
        osal_printk("<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>\\r\\n");
        osal_printk("\\r\\n");
        osal_printk("Hello MYF SparkLine_{project_name.upper()}-number[%d]\\r\\n",CONFIG_{project_name.upper()});
        osal_printk("\\r\\n");
        osal_printk("<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>\\r\\n");
        osDelay({project_name.upper()}_DURATION_MS);
    }}

    return NULL;
}}

static void {project_name.lower()}_test_entry(void)
{{
    osThreadAttr_t attr;

    attr.name = "{project_name.upper()}Task";
    attr.attr_bits = 0U;
    attr.cb_mem = NULL;
    attr.cb_size = 0U;
    attr.stack_mem = NULL;
    attr.stack_size = {project_name.upper()}_TASK_STACK_SIZE;
    attr.priority = {project_name.upper()}_TASK_PRIO;

    if (osThreadNew((osThreadFunc_t){project_name.lower()}_test_task, NULL, &attr) == NULL) {{
        /* Create task fail. */
    }}
}}

/* Run the {project_name.lower()}_test_entry. */
app_run({project_name.lower()}_test_entry);
'''
    
    with open(c_file_path, 'w', encoding='utf-8') as f:
        f.write(c_content)
    
    print(f"已创建: {c_file_path}")

def main():
    parser = argparse.ArgumentParser(description='创建项目工具')
    parser.add_argument('project_name', help='项目名称')
    parser.add_argument('-p', '--parent', help='指定父级用户代码空间名称')
    
    args = parser.parse_args()
    
    project_name = args.project_name
    parent_space = args.parent
    
    # 验证项目名是否符合变量名规则
    if not is_valid_project_name(project_name):
        sys.exit(1)
    
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
    
    # 检查项目是否已存在
    if check_project_exists(project_name, user_project_dir):
        sys.exit(1)
    
    # 1. 更新CMakeLists.txt
    update_cmakelists(project_name, user_project_dir)
    
    # 2. 更新Kconfig
    update_kconfig(project_name, user_project_dir)
    
    # 3. 创建项目目录
    project_dir = create_project_dir(project_name, user_project_dir)
    
    # 4. 创建项目Kconfig
    create_project_kconfig(project_name, project_dir)
    
    # 5. 创建CMakeLists.txt
    create_cmakelists(project_name, project_dir)
    
    # 6. 创建C文件
    create_c_file(project_name, project_dir)
    
    print(f"\n项目 '{project_name}' 在用户代码空间 '{user_project_dir.split('/')[-1]}' 中创建完成!")

if __name__ == "__main__":
    main()        