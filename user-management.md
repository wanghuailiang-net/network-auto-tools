# 查看当前用户和系统信息
whoami                             # 确认当前是 root
id                                  # 查看 UID、GID 和所属组
cat /etc/passwd | head -5           # 查看前5个系统用户
# 创建一个新用户devops
useradd -m -s /bin/bash devops      # -m 创建家目录，-s 指定 shell
passwd devops                       # 设置密码（例如 123456，生产环境请用强密码）
# 赋予dvops sudo权限
usermod -aG sudo devops             # Ubuntu 系统用 sudo 组
# 如果是 CentOS 用 wheel 组：usermod -aG wheel devops
# 切换用户测试
su - devops                         # 切换到 devops 用户
sudo whoami                         # 应输出 root，说明 sudo 成功
exit                                # 退回 root
# 文件权限练习（以root身份）
touch /tmp/testfile                 # 创建测试文件
ls -l /tmp/testfile                 # 查看权限（如 -rw-r--r--）
chmod 600 /tmp/testfile             # 改为只有所有者可读写
ls -l /tmp/testfile                 # 确认权限变为 -rw-------
# 测试权限：切换回devops尝试读文件（应失败）
su - devops
cat /tmp/testfile                    # 应该提示 Permission denied
exit
# 修改文件持有者
groupadd project                     # 创建新组 project
usermod -aG project devops           # 将 devops 加入 project 组
# （可选）创建新组，并将devops文件转过去
groups devops                        # 查看 devops 所属组
chown devops:devops /tmp/testfile    # 将文件所有者和组改为 devops
ls -l /tmp/testfile                  # 确认所有者已变
