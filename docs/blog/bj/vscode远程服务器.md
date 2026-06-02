# VSCode Remote-SSH 无法连接并反复要求输入密码问题详解

## 一、问题现象描述

1、 典型表现

当使用 VS Code 的 Remote-SSH 功能连接远程服务器时：

* 成功输入密码后，VS Code 并未正常连接服务器；
* 系统反复弹出“请输入 SSH 密码”的提示窗口；
* 即使密码无误，连接始终无法建立；
* Terminal 中可能看到 "Retrying after error: Connection refused" 或 "Permission denied" 之类的提示；
* 有时会自动执行安装 VS Code Server 的命令，但无反应或失败。

2、 尝试
* 反复重启 VS Code；
* 更换网络环境；
* 再三确认 SSH 密码是否输入正确；
* 在 ~/.ssh/config 中重新配置主机信息；
* 最后尝试通过命令行使用 ssh user@host 连接远程主机，结果显示一切正常。

但令人困惑的是，即便通过终端可以正常使用 SSH 登录，但用vscode Remote-SSH 插件却依然连接失败。


## 二、原因分析

该问题的根本原因通常并不在于 SSH 配置错误或网络异常，而是出现在 **VS Code 在服务器上部署的 vscode-server 出现异常或损坏。**

Remote-SSH 插件在首次连接服务器时，会自动将一个小型的 vscode-server 程序上传至远程主机的 **~/.vscode-server**目录中，并通过该程序建立编辑器与远程主机之间的通信。

当这个 vscode-server 出现以下情况时就可能导致问题：

* 安装过程中被中断；
* 升级 VS Code 后版本不一致；
* .vscode-server 目录权限错误或文件损坏；
* 残留的临时文件引起冲突；
* 磁盘空间不足或远程主机资源紧张。

## 三、解决方案详解
**1. 首选方式：清除服务器上的 vscode-server**

可以通过清除服务器上的 .vscode-server 目录来强制 VS Code 在下次连接时重新部署该服务。操作步骤如下：

第一步：登录远程服务器（使用其他方法sftp或者终端等）

第二步：删除 .vscode-server 目录

```rm -rf ~/.vscode-server```


>注意：如果使用的是 VS Code Insiders，则目录名可能为 ~/.vscode-server-insiders；也有使用的是 ~/.vscode-remote，需根据具体情况处理。

第三步：重新连接 VS Code Remote-SSH

重新在 VS Code 中打开命令面板（Ctrl + Shift + P），执行：

```Remote-SSH: Connect to Host...```

选择目标主机，系统将重新部署 VS Code Server，并建立新的连接。

## 参考
[https://blog.csdn.net/lph159/article/details/147474689](https://blog.csdn.net/lph159/article/details/147474689)