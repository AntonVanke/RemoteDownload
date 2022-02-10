## RemoteDownload

> RemoteDownload 是使用 Flask 制作的代理下载工具，用来解决网络环境不好的情况下的下载问题(如：github 的国内加速下载)。

### 简单的使用方法

1. 克隆代码到服务器

   ```shell
   git clone https://github.com/AntonVanke/RemoteDownload.git
   ```

2. 安装 `Python` 包

   ```shell
   cd RemoteDownload/
   pip3 install -r requirements.txt
   ```

   如果你没有`Python`

   ```shell
   apt install python3
   # or
   yum install python3
   ```

3. 运行脚本

   ```shell
   python3 app.py
   # ssh 运行 nohup python3 app.py &
   ```

> 如果你执行的没有错误的话，你就可以访问`ip:port`(默认端口是5000)来打开网页。当然，你也可以更改`templates/index.html`来美化首页。
>
> *需要在安全组打开相应的端口*

### Nginx 反代

如果你的服务器有`Nginx`，你也可以通过修改配置文件来共存使用。

```nginx
# ……
server {
        listen       80;
        server_name  www.example.com;
        root /usr/share/nginx/html;
        location / {
        		# 转发到 flask 的 5000
                proxy_pass       http://127.0.0.1:5000;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
# ……
```

修改后使用`sudo nginx -s reload`重载配置。

### 开机自启动

创建文件`/etc/systemd/system/remotedownload.service`，内容如下

```ini
[Unit]
Description=remotedownload
Documentation=https://github.com/AntonVanke/RemoteDownload

[Service]
Type=simple
StandardError=journal
ExecStart="/usr/bin/python3" "#此处写入`app.py`路径#"
ExecReload=/bin/kill -HUP $MAINPID
LimitNOFILE=51200
Restart=on-failure
RestartSec=1s

[Install]
WantedBy=multi-user.target
```

然后执行

```shell
systemctl enable remotedownload
systemctl start remotedownload
```

