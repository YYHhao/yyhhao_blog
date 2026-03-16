# Linux tmux 介绍
tmux（Terminal Multiplexer）是一个终端复用工具，它允许你在单个终端窗口中创建多个虚拟终端会话，并能保持这些会话在后台运行。与直接使用终端相比，tmux 提供了更强大的会话管理功能。

## 使用原因
因为服务器运行代码，服务器终端必须一直挂着，但服务器有时候老师自己中断，这时候后台运行的代码也会中断。**无论是主动退出服务器还是电脑关机都能继续运行代码，为了避免代码运行中断，因此使用tmux。**

## 安装
以我的Ubuntu系统为例
```
sudo apt-get install tmux
```
但报错：
```
bash: sudo: command not found
```
该报错说明我的 Linux 服务器（看起来是 root 用户登录）要么没安装 sudo，要么 sudo 不在环境变量里。由于我当前已是 root 用户（命令行前缀是 root@ai:/#），无需用 sudo，直接用 root 权限安装即可。
```
# 更新软件源（可选，但避免安装失败）
apt update

# 直接安装 tmux（root 用户无需 sudo）
apt install tmux -y
```
验证安装成功：
```
# 查看 tmux 版本
tmux -V

# 启动 tmux（测试）
tmux
```

补充：如果非要用 sudo（可选安装 sudo）
如果后续需要普通用户用 sudo，可先给 root 安装 sudo：
```
# Debian/Ubuntu
apt install sudo -y
```
## tmux简单命令
功能|命令
---|---   
新建|tumx new -s yyh 
退出|先按Ctrl+b,再按d（或者再按：输入detach）
查看|tmux ls
重新进入|tmux attach -t yyh
杀死会话|tmux kill-session -t yyh




参考：
[linux tmux菜鸟教程](https://www.runoob.com/linux/linux-comm-tmux.html)