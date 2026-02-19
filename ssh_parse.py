import paramiko
import re
import json

host = "121.37.152.201"
port = 22
username = "root"
password = "whl104499@"        # 替换为你的密码
remote_file = "/root/switch_config.txt"

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

# 解析代码...
interface_pattern = r'^interface\s+(\S+)'
interfaces = re.findall(interface_pattern, config, re.MULTILINE)

blocks = re.split(r'^!', config, flags=re.MULTILINE)
for block in blocks:
    if block.strip().startswith('interface'):
        lines = block.strip().split('\n')
        iface = lines[0].split()[1]
        desc = None
        for line in lines[1:]:
            if line.strip().startswith('description'):
                desc = line.strip().split('description')[1].strip()
                break
        print(f"接口 {iface} 描述：{desc}")

vlan_ips = {}
pattern = re.compile(r'^interface\s+(Vlan\d+).*?(?=^!)', re.MULTILINE | re.DOTALL)
for match in pattern.finditer(config):
    block = match.group(0)
    iface = match.group(1)
    ip_match = re.search(r'ip address (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)', block)
    if ip_match:
        ip = ip_match.group(1)
        mask = ip_match.group(2)
        vlan_ips[iface] = f"{ip}/{mask}"
        print(f"提取到 {iface} IP: {ip}/{mask}")
    else:
        print(f"警告：接口 {iface} 未找到 IP 配置")

trunk_allowed = {}
trunk_lines = re.findall(r'^interface\s+(\S+).*?switchport trunk allowed vlan ([\d,]+)', 
                         config, re.MULTILINE | re.DOTALL)
for iface, vlans in trunk_lines:
    trunk_allowed[iface] = vlans
    print(f"接口 {iface} 允许的 trunk VLAN: {vlans}")

# 正确的 result 结构
result = {
    "interfaces": interfaces,
    "vlan_ips": vlan_ips,
    "trunk_allowed": trunk_allowed
}

print("\n解析结果 JSON：")
print(json.dumps(result, indent=2, ensure_ascii=False))

with open("parsed_remote_config.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
    print("解析结果已保存到 parsed_remote_config.json")