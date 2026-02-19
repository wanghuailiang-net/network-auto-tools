import paramiko
import os
from datetime import datetime, timedelta
import difflib

# ====== 配置 ======
host = "121.37.152.201"
port = 22
username = "root"
password = "whl104499@"        # 修改为你的密码
remote_file = "/root/switch_config.txt"
backup_base = "backups"         # 备份根目录

# ====== 创建今天的备份目录 ======
today = datetime.now().strftime("%Y-%m-%d")
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
today_dir = os.path.join(backup_base, today)
yesterday_dir = os.path.join(backup_base, yesterday)
os.makedirs(today_dir, exist_ok=True)

# ====== SSH 获取配置 ======
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print(f"正在连接 {host} ...")
    client.connect(host, port, username, password, timeout=5)
    print("连接成功")

    command = f"cat {remote_file}"
    stdin, stdout, stderr = client.exec_command(command)
    config = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')

    if error:
        print("远程命令执行错误：", error)
        exit(1)
    else:
        print("配置文件获取成功，长度：", len(config))

finally:
    client.close()
    print("SSH 连接已关闭")

# ====== 保存今天的配置 ======
today_file = os.path.join(today_dir, "switch_config.txt")
with open(today_file, "w", encoding="utf-8") as f:
    f.write(config)
print(f"已保存到 {today_file}")

# ====== 检查昨天的配置是否存在 ======
yesterday_file = os.path.join(yesterday_dir, "switch_config.txt")
if os.path.exists(yesterday_file):
    with open(yesterday_file, "r", encoding="utf-8") as f:
        old_config = f.read()

    if old_config == config:
        print("配置无变化")
    else:
        print("配置已变更，差异如下：")
        diff = difflib.unified_diff(
            old_config.splitlines(),
            config.splitlines(),
            fromfile=f"昨天 ({yesterday})",
            tofile=f"今天 ({today})",
            lineterm=""
        )
        diff_text = "\n".join(diff)
        print(diff_text)

        # 保存差异到日志
        log_file = os.path.join(today_dir, "changes.log")
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(diff_text)
        print(f"变更记录已保存到 {log_file}")
else:
    print("昨天没有备份，无法对比")