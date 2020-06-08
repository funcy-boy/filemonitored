# 使用须知

### 环境依赖
```bash
pip install -r requirementes.txt
```

### 将angent.py打包成exe文件

```
pyinstaller.exe -F agent.py
```

- exe文件会在`dist`目录生成

### 配置文件

```bash
[Global]
WechatBot = xxx #企业微信机器人地址
Post_Url = http://xxxx/pull_event  #服务端post地址
Website_Path = ['D:\EFI\WEB_B2B','D:\EFI\WEB_B2C']  #配置要监控的目录
```

### 安装服务

```bash
agent.exe --startup auto install    #注册开机自启动
agent.exe start #开启服务
```
- 安装好的服务可在windows服务列表里查看