# https://github.com/vsantiago113/RuckusVirtualSmartZoneAPIClient
import RuckusVirtualSmartZoneAPIClient
import  json
# client = RuckusVirtualSmartZoneAPIClient.Client()
client = RuckusVirtualSmartZoneAPIClient.Client(verify=False, warnings=False, api_version='v9_1')
client.connect(url='https://172.16.0.127:8443', username='admin', password='Admin@123')

response = client.get(method='/domains')
domain_id = response.json()['id']
print(json.dumps(response.json(), indent=4)) # --> 201

response = client.post(method='/domains', data={'name': 'TestDomain'})
domain_id = response.json()['id']
print(json.dumps(response.json(), indent=4)) # --> 201

client.disconnect()

print("test1 completed")

def getClient():
    client = RuckusVirtualSmartZoneAPIClient.Client()
    client.connect(url='https://172.16.0.127:8443', username='admin', password='Admin@123')
    return client

if __name__ == '__main__':
    c = getClient()
    c.disconnect()

# client.headers
# client.base_url
# client.token
# client.auth
# client.server
