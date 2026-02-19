import re
import json

# 读取配置文件
with open('switch_config.txt', 'r') as f:
    config = f.read()

print("配置文件读取成功，长度：", len(config))

# 1. 提取所有接口名
interface_pattern = r'^interface\s+(\S+)'
interfaces = re.findall(interface_pattern, config, re.MULTILINE)
print("找到的接口：", interfaces)

# 2. 分割配置块（按 '!' 分割），提取接口描述
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

# 3. 提取 VLAN 接口的 IP 地址
vlan_ips = {}
# 匹配每个 VLAN 接口的完整段落（从 "interface VlanX" 到下一个 "!" 之前）
pattern = re.compile(r'^interface\s+(Vlan\d+).*?(?=^!)', re.MULTILINE | re.DOTALL)
for match in pattern.finditer(config):
    block = match.group(0)        # 整个接口块内容
    iface = match.group(1)        # 接口名，如 Vlan10
    # 在块内查找 IP 地址
    ip_match = re.search(r'ip address (\d+\.\d+\.\d+\.\d+) (\d+\.\d+\.\d+\.\d+)', block)
    if ip_match:
        ip = ip_match.group(1)
        mask = ip_match.group(2)
        vlan_ips[iface] = f"{ip}/{mask}"
        print(f"提取到 {iface} IP: {ip}/{mask}")
    else:
        print(f"警告：接口 {iface} 未找到 IP 配置")

# 4. 提取 trunk 允许的 VLAN
trunk_allowed = {}
trunk_lines = re.findall(r'^interface\s+(\S+).*?switchport trunk allowed vlan ([\d,]+)', config, re.MULTILINE | re.DOTALL)
for iface, vlans in trunk_lines:
    trunk_allowed[iface] = vlans
    print(f"接口 {iface} 允许的 trunk VLAN: {vlans}")

# 5. 构造最终结果字典（所有值都是 JSON 可序列化的）
result = {
    "interfaces": interfaces,
    "vlan_ips": vlan_ips,
    "trunk_allowed": trunk_allowed
}

# 6. 输出漂亮的 JSON
print(json.dumps(result, indent=2, ensure_ascii=False))