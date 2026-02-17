# 2026.2.17 第一次在云服务器部署 nginx
- 用华为云 CloudShell 登录服务器（root 密码登录whl104499@）
- 执行命令：
  apt update && apt install nginx -y           #更新软件源并安装nginx
  systemctl start nginx                        #立即启动nginx
  systemctl enable nginx                       #将nginx设为开机自启
- 在控制台放行 80 端口                          #确认active
- 浏览器访问 http://121.37.152.201 看到欢迎页