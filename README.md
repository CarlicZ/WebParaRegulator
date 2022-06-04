# WebParaRegulator

此为深圳大学RoboPilots网页调参项目

[toc]

# 项目简介

要想使用本项目，需要关注以下三个主要程序：

-   `data_api.py`：基于flask开发的服务器python程序
-   `WebParaClient.py`：基于python的客户端程序
-   `demo.py` ：基于python的模拟读程序流程

其中 `demo.py` 详细说明了应用程序如何与 `WebParaClient.py` 交互的详细流程，可以自行设计自己应用中的流程来读取参数。

项目交互的方式如下图所示：

![网页调参工作原理](https://smcbaq-picture.oss-cn-guangzhou.aliyuncs.com/images_2/picgo/aliyunOSS%E7%BD%91%E9%A1%B5%E8%B0%83%E5%8F%82%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86.jpg)

其他重要文件：

-   `car_conf.py `、`read_flag.py`：客户端交互文件
-   `RP_car_data.db`：存储车辆参数数据库
-   `index.html`、`car.html`：调参网页

# 安装使用

1. 依赖包安装：

    ```bash
    pip install -r requirements.txt
    ```

2.   服务端安装：

     方法1：直接运行（注意退出终端的进程结束问题）

     ```bash
     python data_api.py
     ```

     方法2：使用`systemd`进行进程守护（linux下）

     1.   修改 `systemd/WebParaServer.service` 文件中的**路径**和**用户名**，路径请务必使用绝对路径
     2.   将`systemd/WebParaServer.service` 文件复制到 `/etc/systemd/system`文件夹下
     3.   使用命令 `sudo systemctl start WebParaServer`启动服务
     4.   若修改了 `*.service` 文件重新复制，需要使用 `sudo systemctl daemon-reload` 重载一下

3.   客户端安装：

     与服务端方法2差不多，使用`systemd`进行进程守护（linux下）

     1.   修改 `systemd/WebParaClient.service` 文件中的**路径**和**用户名**，路径请务必使用绝对路径
     2.   将`systemd/WebParaClient.service` 文件复制到 `/etc/systemd/system`文件夹下
     3.   使用命令 `sudo systemctl start WebParaClient`启动服务
     4.   若修改了 `*.service` 文件重新复制，需要使用 `sudo systemctl daemon-reload` 重载一下
     5.   可选：使用命令 `sudo systemctl enable WebParaClient`启动开机自启

# 效果

## 主界面

![image-20220604165535654](https://smcbaq-picture.oss-cn-guangzhou.aliyuncs.com/images_2/picgo/aliyunOSSimage-20220604165535654.png)

功能：

-   添加车辆
-   删除车辆
-   前往车辆参数页面

# 车辆界面



![image-20220604165520404](https://smcbaq-picture.oss-cn-guangzhou.aliyuncs.com/images_2/picgo/aliyunOSSimage-20220604165520404.png)

功能：

-   添加参数：参数名、类、值
-   修改参数值
-   删除参数
