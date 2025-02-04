import requests
import json

# Only use when testing, surpresses warnings about insecure servers
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

session = requests.Session()
jar = requests.cookies.RequestsCookieJar()

baseurl = "https://172.16.0.127:8443/wsg/api/public/v9_1/"

# Written with 3.6.2 in mind

#http://docs.ruckuswireless.com/smartzone/3.6.2/sz100-public-api-reference-guide-3-6-2.html API documentation

sz_username = "admin"
sz_password = "Admin@123"  # Password for the above account
check_cert = False  # True # Change to false if using selfsigned certs or cert chain is not on the machine running the script

login_headers_template = {'Content-Type': "application/json;charset=UTF-8"}

login_payload = '{  "username": "' + sz_username + '",\r\n  "password": "' + sz_password + '"}'

def ruckus_login(url,data):
    output = session.post(baseurl + url, data=data, headers=login_headers_template, verify=check_cert)
    return output
#This uses the ruckus_post above to get a session valid session cookie into the cookie jar
get_login_session_cookie = ruckus_login("session", login_payload)
jar = get_login_session_cookie.cookies

headers_template = {
                    'Content-Type': "application/json;charset=UTF-8",
                    'Cookie': 'JSESSIONID='+ jar['JSESSIONID']
                    }

def ruckus_post(url,data):
    output = session.post(baseurl + url, data=data, headers=headers_template, verify=check_cert)
    return output

def ruckus_get(url):
    output = session.get(baseurl + url, headers=headers_template, verify=check_cert)
    return output

jsonzones = ruckus_get("rkszones") #Get the JSON data for the zones confiured on the cluster

#The below function ruckus_list is used for stripping out the "list" dictionary from the returned JSON
def ruckus_list(jsondata):
    output = {}
    output = json.loads(jsondata.text)
    output = output["list"]
    return output

zones = ruckus_list(jsonzones)

def clean_ruckus_list(dictdata,dict_parent_name = "NONE",dict_parent_id = "NONE",names="name",ids="id"):
    output = []
    for row in dictdata:
        output_name = ""
        output_id = ""
        for key,val in row.items():
            if key == ids:
                output_id = row[key]
            elif key == names:
                output_name = row[key]
        if dict_parent_name and dict_parent_id == "NONE":
            output.append([output_name,output_id]) #Produce a list without useless data but catch if someone doesn't pass both arguements
        else:
            output.append([dict_parent_name,dict_parent_id,output_name,output_id])
    return output

cleaned_zones = clean_ruckus_list(zones)

cleaned_all_zone_wlan = []

for row in cleaned_zones:
    zone_id = row[1]
    zone_name = row[0]
    urltemplate = "rkszones/{}/wlans"
    jsonwlan = ruckus_get(urltemplate.format(zone_id))
    wlan = ruckus_list(jsonwlan)
    cleaned_all_zone_wlan.extend(clean_ruckus_list(wlan,zone_name,zone_id))

print("\n")
print("-" * 50)
print("\n")
print("The WLANs configured on this szcluster are:")
print("\n")
zone_print = ""
for row in cleaned_all_zone_wlan:
    if zone_print == row[0]:
        print("    Name: {} and ID: {}".format(row[2],row[3]))
    else:
        zone_print = row[0]
        print("-" * 5)
        print("\n")
        print(row[1])
        print("{} zone's WLAN are:".format(row[0]))
        print("\n")
        print("    Name: {} and ID: {}".format(row[2],row[3]))
print("\n")
print("-" * 50)
