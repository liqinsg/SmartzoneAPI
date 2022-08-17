import requests
import json
# https://docs.ruckuswireless.com/smartzone/5.2.2/sz100-public-api-reference-guide-522.html

# Only use when testing, surpresses warnings about insecure servers
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

session = requests.Session()
jar = requests.cookies.RequestsCookieJar()

# replace "general.direction.com" with either the host name or IP of a member of the cluster
# baseurl = "https://172.16.0.127:8443/wsg/api/public/v9_1/"
baseurl = "https://192.168.56.3:8443/wsg/api/public/v9_1/"

# Written with 3.6.2 in mind
# http://docs.ruckuswireless.com/smartzone/3.6.2/sz100-public-api-reference-guide-3-6-2.html API documentation

# Enter a username with read privages to everything you want to access
# sz_username = "admin"
# sz_password = "Admin@123"  # Password for the above account
sz_username = "admin"
sz_password = "F@r3astovh"  # Password for the above account

check_cert = False  # True # Change to false if using selfsigned certs or cert chain is not on the machine running the script

login_headers_template = {'Content-Type': "application/json;charset=UTF-8"}

login_payload = '{  "username": "' + sz_username + '",\r\n  "password": "' + sz_password + '"}'

credential = {"username": sz_username, "password": sz_password}


def ruckus_login(url: str, jsondata: {}):
    output = session.post(baseurl + url, json=jsondata,
                          headers=login_headers_template, verify=check_cert)
    return output


def ruckus_login_json(url="session", jsondata={}):
    """
    :param url: endpoint
    :param jsondata: json
    :return:
    """
    output = session.post(baseurl + url, json=jsondata,
                          headers=login_headers_template, verify=check_cert)
    return output


# This uses the ruckus_post above to get a session valid session cookie into the cookie jar
# get_login_session_cookie = ruckus_login("session", login_payload)
get_login_session_cookie = ruckus_login_json("session", credential)

jar = get_login_session_cookie.cookies

headers_template = {
    'Content-Type': "application/json;charset=UTF-8",
    'Cookie': 'JSESSIONID=' + jar['JSESSIONID']
}


def ruckus_post(url: str, jsondata={}):
    """
    :param jsondata:
    :type url: object
    """
    _url = baseurl + url
    output = session.post(_url, json=jsondata,
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


def get_zones():
    # Get the JSON data for the zones confiured on the cluster
    zone_list = []
    jsonzones = ruckus_get("rkszones")

    zones = ruckus_list(jsonzones)

    cleaned_zones = clean_ruckus_list(zones)

    print("\n")
    print("-" * 50)
    print("\n")
    print("The zones configured on this szcluster are:")
    print("\n")
    # z = {"name": '', "id":""}
    for row in cleaned_zones:
        print("Name: {} and ID: {}".format(row[0], row[1]))
        # z = {"name": row[0], "id": row[1]}
        # zone_list.append(z)
        print("-" * 5)
    print("\n")
    print("-" * 50)
    return zones


def get_ap_groups(zoneid: str):
    '''
    The zones configured on this szcluster are:
    Name: Default Zone-5.2.2 and ID: 6d037318-ea21-464a-adbe-d5934ebc17a7
    -----
    Name: New FW-5.2.2 and ID: d1097983-6a64-4393-9a80-1cff0096e1b5
    -----
    Name: ORS and ID: b07d6c2c-979b-4d0f-87d8-f5c5b11b81a7
    -----
    Name: Default Zone and ID: f77a8816-3049-40cd-8484-82919275ddc3
    -----
    '''
    # zoneid = '979b04d3-6a94-4730-adb8-8c211cd26bb4'
    # zoneid = '6d037318-ea21-464a-adbe-d5934ebc17a7'
    url = 'rkszones/%s/apgroups' % zoneid
    jsdata = ruckus_get(url)
    ag = ruckus_list(jsdata)
    print(ag)
    return jsdata
    # print(cleaned_zones = clean_ruckus_list(ag))

    # print(resp)
    # return resp


def create_apgroup(json_data):
    zoneid = '979b04d3-6a94-4730-adb8-8c211cd26bb4'
    url = 'rkszones/%s/apgroups' % zoneid
    data = {
        "name": "myapGroup",
        "description": "apGroupHere"
    }
    jsdata = ruckus_post(url, json_data)
    return jsdata


def reboot_system():
    '''
    for cluster, which node to reboot?
    may need to get system information to identify the node
    e.g. wlc1, wlc2 or wlc3
    '''
    _url = baseurl + 'restart'
    output = session.post(_url,
                          headers=headers_template, verify=check_cert)
    return output

    # jsdata = ruckus_post('restart', {})
    # return jsdata


# test code

z_list = get_zones()
r = get_ap_groups('6d037318-ea21-464a-adbe-d5934ebc17a7')

# data = {
#     "name": "myapGroup",
#     "description": "apGroupHere"
# }
# r = create_apgroup(data)
# r = reboot_system()
if r.ok:
    json_data = ruckus_list(r)
    print(r)
else:
    print(r.content)
