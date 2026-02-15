from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkvpc.v2 import VpcClient, ListVpcsRequest
from huaweicloudsdkcore.region.region import Region

# ========== 你的华为云账号信息（从CSV复制）==========
ak = "HPUAWO3VSSAME5710CS3"
sk = "hHU0BD39AEpYkWcpYBugX8Rcz4B0I3TCjJYfQaBw"
region_id = "cn-east-3"
# =================================================

if __name__ == "__main__":
    credentials = BasicCredentials(ak, sk)

    client = VpcClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(Region(region_id, f"https://vpc.{region_id}.myhuaweicloud.com")) \
        .build()

    request = ListVpcsRequest()
    response = client.list_vpcs(request)

    print("=" * 50)
    print("当前账号下的VPC列表：")
    print("=" * 50)

    for vpc in response.vpcs:
        print(f"名称: {vpc.name}")
        print(f"ID: {vpc.id}")
        print(f"网段: {vpc.cidr}")
        print(f"状态: {vpc.status}")
        print("-" * 30)