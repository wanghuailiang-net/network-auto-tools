import csv
from netmiko import ConnectHandler
from concurrent.futures import ThreadPoolExecutor
import os
from datetime import datetime

# 创建备份目录（以时间戳命名）
backup_dir = f"backups_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(backup_dir, exist_ok=True)

# 读取设备列表
devices = []
with open('devices.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        devices.append(row)

def backup_device(device):
    """备份单台设备"""
    try:
        print(f"正在连接 {device['ip']}...")
        conn = ConnectHandler(
            device_type=device['device_type'],
            host=device['ip'],
            username=device['username'],
            password=device['password'],
            timeout=10
        )
        # 根据设备类型选择命令
        if device['device_type'] == 'linux':
            command = 'cat /root/switch_config.txt'
        elif device['device_type'] == 'huawei':
            command = 'display current-configuration'
        elif device['device_type'] == 'cisco_ios':
            command = 'show running-config'
        else:
            command = 'display current-configuration'  # 默认
        output = conn.send_command(command, expect_string=r'[#$>]')
        conn.disconnect()
        
        # 保存到文件
        filename = os.path.join(backup_dir, f"{device['ip']}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"{device['ip']} 备份成功 -> {filename}")
        return True
    except Exception as e:
        print(f"{device['ip']} 备份失败: {str(e)}")
        return False

# 并发执行（最多同时5个线程）
with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(backup_device, devices))

print(f"备份完成，成功 {sum(results)} 台，失败 {len(results)-sum(results)} 台")