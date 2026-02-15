from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkecs.v2 import EcsClient, ListServersDetailsRequest
from huaweicloudsdkcore.region.region import Region

# ========== 你的华为云账号信息（从CSV复制）==========
ak = "HPUAWO3VSSAME5710CS3"
sk = "hHU0BD39AEpYkWcpYBugX8Rcz4B0I3TCjJYfQaBw"
region_id = "cn-east-3"
# =================================================

if __name__ == "__main__":
    credentials = BasicCredentials(ak, sk)

    client = EcsClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(Region(region_id, f"https://ecs.{region_id}.myhuaweicloud.com")) \
        .build()

    request = ListServersDetailsRequest()
    request.limit = 10  # 可选，限制返回数量
    response = client.list_servers_details(request)

    print("=" * 50)
    print("当前账号下的ECS列表：")
    print("=" * 50)

    if response.servers:
        for server in response.servers:
            print(f"名称: {server.name}")
            print(f"ID: {server.id}")
            print(f"状态: {server.status}")
            # 安全获取规格名称
            flavor_name = server.flavor.name if server.flavor else 'N/A'
            print(f"规格: {flavor_name}")
            print("-" * 30)
    else:
        print("没有找到ECS实例。")