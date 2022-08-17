import requests
import warnings
warnings.filterwarnings("ignore", message= "Unverified HTTPS request ")
host = 'https://172.16.0.127:8443'
baseurl = "https://172.16.0.127:8443/wsg/api/public/v9_1/"

username = "admin"
password = "Admin@123"
r = requests.Session()

#Get authentication token
tkurl = 'serviceTicket'
response = r.post(baseurl +  tkurl, json={'username': username, 'password': password}, verify=False).json()
serviceTicket = response['serviceTicket']
print(serviceTicket)

#Create apgroup
def create_appgroup(zoneid, data):
    zoneid = '979b04d3-6a94-4730-adb8-8c211cd26bb4'
    url = baseurl + 'rkszones/%s/apgroups' % zoneid
    data = {'name': 'TexasAPGroup2'}
    response = r.post(url + '?serviceTicket=' + serviceTicket, json=data, verify=False)
    print(response.json())

# reboot system
url = baseurl + '/restart'
response = r.post(url + '?serviceTicket=' + serviceTicket, verify=False)
print(response.json())

#Create domain
response = r.post(baseurl + 'domains?serviceTicket=' + serviceTicket, json={'name': 'Texas'}, verify=False)
# response = r.post(baseurl + 'domains?serviceTicket=' + serviceTicket, json={'name': 'Texas'}, verify=False).json()
print(response.json())
domainId = response['id']
print(domainId)

#Create zone
response = r.post(host + '/wsg/api/public/v9_0/rkszones?serviceTicket=' + serviceTicket, json={'domainId': domainId,'name': 'Dallas','description': '',
'countryCode': 'US','login': {'apLoginName': 'admin','apLoginPassword': 'ruckus123!'},'apHccdEnabled': True}, verify=False).json()
zoneId = response['id']
print(zoneId)

#Create AP
response = r.post(host + '/wsg/api/public/v9_0/aps?serviceTicket=' + serviceTicket, json={'mac': '00:11:22:33:44:56','zoneId': zoneId ,'serial': '00000123',
'model': 'R750','name': 'R750-A','location': 'San Jose','description': 'My first R750'}, verify=False)

#Query AP
response = r.post(host + '/wsg/api/public/v9_0/query/ap?serviceTicket=' + serviceTicket, json={'filters': [{'type': 'ZONE','value': zoneId}]},
verify=False).json()
apMacAddress = response['list'][0]['apMac']
print(apMacAddress)

#Create wlan
response = r.post(host + '/wsg/api/public/v9_0/rkszones/' + zoneId + '/wlans?serviceTicket=' + serviceTicket, json={"name": "Eiriksson",
"ssid": "Eiriksson","description": "my wlan","encryption": {"method": "WPA2","algorithm": "AES","passphrase": "ruckus123"},"advancedOptions":
{"clientFingerprintingEnabled": True,"avcEnabled": True}}, verify=False).json()
wlanId = response['id']
print(wlanId)
