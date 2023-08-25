import ipaddress
import tldextract
import re

# 从文件中读取样本数据
with open('res.txt', 'r') as file:
    data = file.read().splitlines()

# 正则表达式模式
private_ip_networks = [
    ipaddress.IPv4Network('10.0.0.0/8'),
    ipaddress.IPv4Network('172.16.0.0/12'),
    ipaddress.IPv4Network('192.168.0.0/16')
]

# 初始化集合
private_ips = set()
valid_internet_ips = set()
domains = set()
root_domains = set()
urls = set()

for line in data:
    try:
        ip = ipaddress.ip_address(line)
        if any(ip in net for net in private_ip_networks):
            private_ips.add(str(ip))
        else:
            valid_internet_ips.add(str(ip))
    except ValueError:
        # 使用 tldextract 库提取域名
        domain_info = tldextract.extract(line)
        if domain_info.registered_domain:
            domains.add(domain_info.registered_domain)
            root_domain = '.'.join([part for part in domain_info.subdomain.split('.') if part])
            if root_domain:
                root_domain += '.' + domain_info.registered_domain
                root_domains.add(root_domain)

        # 使用正则表达式提取URL
        url_pattern = r'https?://[^\s/$.?#].[^\s]*'
        urls.update(re.findall(url_pattern, line))

# 将结果保存到文件
with open('private_ip.txt', 'w') as file:
    file.write('\n'.join(private_ips))

with open('inter_ip.txt', 'w') as file:
    file.write('\n'.join(valid_internet_ips))

with open('domain.txt', 'w') as file:
    file.write('\n'.join(domains))

with open('rootdomain.txt', 'w') as file:
    file.write('\n'.join(root_domains))

with open('urls.txt', 'w') as file:
    file.write('\n'.join(urls))

print("私网IP已保存到 private_ip.txt")
print("互联网IP已保存到 inter_ip.txt")
print("域名已保存到 domain.txt")
print("根域名已保存到 rootdomain.txt")
print("URL已保存到 urls.txt")
