# miniconda和conda优先级问题

## 问题原因
服务器老是系统资源不足，我在数据路径下，下载了miniconda，但使用conda 命令还是原先系统路径的anaconda，为了不更改服务器文件，在不删除anaconda的前提下让miniconda优先。

## 解决问题

**直接用 vim 编辑 .bashrc（推荐，无需安装）
vim 是 Linux 系统默认自带的编辑器，步骤如下：**
```
# 用 vim 打开 .bashrc 文件
vim ~/.bashrc
```
**vim 编辑操作步骤：**   
1、打开文件后，按 i 键进入编辑模式（左下角会显示 INSERT）。   
2、在文件最顶部输入以下内容（替换为你的 Miniconda 实际路径）：
```
# 让 Miniconda 优先于 Anaconda
export PATH="/root/miniconda3/bin:$PATH"  
```
（root 用户的 Miniconda 默认路径是 /root/miniconda3，如果你的路径不同，替换成实际路径）。      
3、编辑完成后，按 Esc 键退出编辑模式。   
4、输入 :wq 并按回车（含义：w= 保存，q= 退出）。   
**使配置生效：**
```
source ~/.bashrc
```

**验证配置是否成功**
```
# 查看 conda 命令路径（应指向 miniconda3）
which conda

# 查看 conda 版本
conda --version
```
输出：
```
/root/miniconda3/bin/conda
conda 24.3.0
```

## conda init 问题
我们使miniconda优先后直接激活虚拟  conda activate myenv报错：
```
CondaError: Run 'conda init' before 'conda activate'
```
**第一步：理解问题原因**    
conda activate 依赖 conda 对终端的初始化脚本，你之前注释了 Anaconda 的初始化，但 Miniconda 还没执行 conda init，导致终端不识别 activate 命令。  
**第二步：解决步骤（针对 Miniconda）**   
1、先执行 Miniconda 的 conda init   
用 Miniconda 的绝对路径执行初始化（避免调用到 Anaconda 的 conda）：
```
# 替换为你的 Miniconda 实际路径（root 用户默认是 /root/miniconda3）
/root/miniconda3/bin/conda init bash
```    
执行后会输出类似内容（表示成功给 bash 终端初始化 Miniconda）：    
```
no change     /root/miniconda3/condabin/conda
no change     /root/miniconda3/bin/conda
no change     /root/miniconda3/bin/conda-env
no change     /root/miniconda3/bin/activate
no change     /root/miniconda3/bin/deactivate
modified      /root/.bashrc

==> For changes to take effect, close and re-open your current shell. <==
```
2、 重新加载配置（或重启终端）  
```
# 重新加载 .bashrc
source ~/.bashrc

# （可选）如果仍有问题，关闭当前终端，重新登录服务器（最彻底）
```
3、验证 conda activate 是否可用   
先测试激活 Miniconda 的 base 环境：
```
conda activate myenv
成功后终端前缀会变成 (myenv)，说明激活功能正常。
```