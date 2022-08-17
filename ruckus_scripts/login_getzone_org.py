import requests
import json

# Only use when testing, surpresses warnings about insecure servers
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

session = requests.Session()
jar = requests.cookies.RequestsCookieJar()

# replace "general.direction.com" with either the host name or IP of a member of the cluster
baseurl = "https://192.168.56.3:8443/wsg/api/public/v9_1/"

# Written with 3.6.2 in mind
# http://docs.ruckuswireless.com/smartzone/3.6.2/sz100-public-api-reference-guide-3-6-2.html API documentation

# Enter a username with read privages to everything you want to access
sz_username = "admin"
sz_password = "F@r3astovh"  # Password for the above account
check_cert = False  # True # Change to false if using selfsigned certs or cert chain is not on the machine running the script

login_headers_template = {'Content-Type': "application/json;charset=UTF-8"}

login_payload = '{  "username": "' + sz_username + '",\r\n  "password": "' + sz_password + '"}'


def ruckus_login(url, data):
    output = session.post(baseurl + url, data=data,
                          headers=login_headers_template, verify=check_cert)
    return output


# This uses the ruckus_post above to get a session valid session cookie into the cookie jar
get_login_session_cookie = ruckus_login("session", login_payload)
jar = get_login_session_cookie.cookies

headers_template = {
    'Content-Type': "application/json;charset=UTF-8",
                    'Cookie': 'JSESSIONID=' + jar['JSESSIONID']
}


def ruckus_post(url, data):
    output = session.post(baseurl + url, data=data,
                          headers=headers_template, verify=check_cert)
    return output


def ruckus_get(url):
    output = session.get(
        baseurl + url, headers=headers_template, verify=check_cert)
    return output

# The below function ruckus_list is used for stripping out the "list" dictionary from the returned JSON
def ruckus_list(jsondata):
    output = {}
    output = json.loads(jsondata.text)
    output = output["list"]
    return output


def clean_ruckus_list(dictdata, dict_parent_name="NONE", dict_parent_id="NONE", names="name", ids="id"):
    output = []
    for row in dictdata:
        output_name = ""
        output_id = ""
        for key, val in row.items():
            if key == ids:
                output_id = row[key]
            elif key == names:
                output_name = row[key]
        # Produce a list without useless data but catchs if someone doesn't pass both arguements
        if dict_parent_name and dict_parent_id == "NONE":
            output.append([output_name, output_id])
        else:
            output.append(
                [dict_parent_name, dict_parent_id, output_name, output_id])
    return output


# Get the JSON data for the zones confiured on the cluster
jsonzones = ruckus_get("rkszones")

zones = ruckus_list(jsonzones)

cleaned_zones = clean_ruckus_list(zones)

print("\n")
print("-" * 50)
print("\n")
print("The zones configured on this szcluster are:")
print("\n")
for row in cleaned_zones:
    print("Name: {} and ID: {}".format(row[0], row[1]))
    print("-" * 5)
print("\n")
print("-" * 50)
