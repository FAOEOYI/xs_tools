 xs 命令使用帮助文档
=====================================================================
xs 是一个便捷的命令行工具，用于简化开发过程中的常见操作，如用户代码空间管理、项目创建与删除、编译和配置等。

使用方法:

```shell
  xs [子命令] [选项]
```

子命令列表:

```shell
  make-user-space    创建用户代码空间
  create-project     创建项目
  clean-user-space   删除用户代码空间
  clean-project      删除项目
  b                  可选择式编译
  build              启动 ws63-liteos-app 目标编译
  menu               可选择式启动目标的 menuconfig 图形配置界面
  menuconfig         启动 ws63-liteos-app 目标的 menuconfig 图形配置界面
  -h                 显示简要帮助信息
  --help             显示此详细帮助信息
```

子命令详细说明及示例:

### 用户代码空间管理
#### 创建默认用户代码空间
```
  描述: 创建名为 user_project 的默认用户代码空间。
  命令: xs make-user-space
  示例: xs make-user-space
```

#### 创建自定义名称用户代码空间
```
  描述: 创建一个指定名称的用户代码空间。
  命令: xs make-user-space <用户代码空间名>
  示例: xs make-user-space TEST001
```

#### 删除指定用户代码空间
```
  描述: 删除指定名称的用户代码空间。
  命令: xs clean-user-space <用户代码空间名>
  示例: xs clean-user-space TEST001
```

#### 强制删除指定用户代码空间
```
  描述: 强制删除指定名称的用户代码空间，忽略可能的错误提示。
  命令: xs clean-user-space <用户代码空间名> -f
  示例: xs clean-user-space TEST001 -f
```

### 项目管理
#### 在默认用户代码空间创建项目
```
  描述: 在默认的 user_project 代码空间中创建一个项目。
  命令: xs create-project <项目名>
  示例: xs create-project T_001
```

#### 在指定用户代码空间创建项目
```
  描述: 在指定名称的用户代码空间中创建一个项目。
  命令: xs create-project <项目名> -p <用户代码空间名>
  示例: xs create-project T_001 -p TEST001
```

#### 删除默认用户代码空间的项目
```
  描述: 删除默认的 user_project 代码空间中的指定项目。
  命令: xs clean-project <项目名>
  示例: xs clean-project T_001
```

#### 删除指定用户代码空间的项目
```
  描述: 删除指定名称的用户代码空间中的指定项目。
  命令: xs clean-project <项目名> -p <用户代码空间名>
  示例: xs clean-project T_001 -p TEST001
```

### 编译与配置
#### 可选择式增量编译
```
  描述: 进行可选择式的增量编译。
  命令: xs b
  示例: xs b
```

#### 可选择式全量编译
```
  描述: 进行可选择式的全量编译。
  命令: xs b -c
  示例: xs b -c
```

#### 启动 ws63-liteos-app 目标的增量编译
```
  描述: 启动 ws63-liteos-app 目标的增量编译。
  命令: xs build
  示例: xs build
```

#### 启动 ws63-liteos-app 目标的全量编译
```
  描述: 启动 ws63-liteos-app 目标的全量编译。
  命令: xs build -c
  示例: xs build -c
```

#### 可选式启动目标的 menuconfig 图形配置界面
```
  描述: 启动可选择式目标的 menuconfig 图形配置界面。
  命令: xs menu
  示例: xs menu
```

#### 启动 ws63-liteos-app 目标的 menuconfig 图形配置界面
```
  描述: 启动 ws63-liteos-app 目标的 menuconfig 图形配置界面。
  命令: xs menuconfig
  示例: xs menuconfig
```

### 项目查找
#### 查找所有项目
```
  描述: 查找所有存在的项目。
  命令: xs find all
  示例: xs find all
```

#### 查找指定代码空间的项目
```
  描述: 查找指定代码空间中的项目。
  命令: xs find <代码空间>
  示例: xs find TEST001
```

xs 命令索引
=====================================================================

```shell
xs -h                                         【帮助】
xs --help                                     【详细帮助】
xs b                                          【可选择式增量编译指令】
xs b -c                                       【可选择式全量编译指令】
xs menu                                       【可选择式启动目标的menuconfig图形配置界面】
xs build                                      【启动 ws63-liteos-app 目标的增量编译指令】
xs build -c                                   【启动 ws63-liteos-app 目标的全量编译指令】
xs menuconfig                            	  【启动 ws63-liteos-app 目标的menuconfig图形配置界面】
xs make-user-space                            【创建默认用户代码空间】
xs make-user-space <用户代码空间名>              【创建自定义名称用户代码空间】
xs create-project <项目名>                     【在默认用户代码空间创建项目】
xs create-project <项目名> -p <用户代码空间名>   【在指定用户代码空间创建项目】
xs clean-user-space <用户代码空间名>           【删除指定用户代码空间】
xs clean-user-space <用户代码空间名> -f        【强制删除指定用户代码空间】
xs clean-project <项目名>                     【删除默认用户代码空间的项目】
xs clean-project <项目名> -p <用户代码空间名>   【删除指定用户代码空间的项目】
xs find all                                  【查找所有项目】
xs find <代码空间>                            【查找指定代码空间的项目】
```

# xs_tools移植指南

- 将`xs_tools`克隆在海思fbb代码仓的SDK目录，可以看到`application`和`build.py`等文件；
- 进入`xs_tools`执行：

```shell
./command_deployment.sh 
```

- 移植成功；

# 开始使用方法

- 在海思fbb代码仓的SDK目录，可以看到`application`和`build.py`等文件；
- 执行：

```shell
. ./set_xs.sh
```

即可使用上面的命令了；

# -END-