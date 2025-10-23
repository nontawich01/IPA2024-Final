import json
import requests
requests.packages.urllib3.disable_warnings()

# Router IP Address
router_ip = "10.0.15.65"  
api_base = f"https://{router_ip}/restconf/data/ietf-interfaces:interfaces"


headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

basicauth = ("admin", "cisco")

def get_interface_config(if_name):
    """
    ตรวจสอบว่า interface มีอยู่ใน config หรือไม่ (GET)
    คืนค่า True ถ้าพบ, False ถ้าไม่พบ (404), หรือ None ถ้ามีปัญหาอื่น
    """
    url = f"{api_base}/interface={if_name}?fields=name"
    try:
        resp = requests.get(url, auth=basicauth, headers=headers, verify=False, timeout=10)
        if resp.status_code == 200:
            return True 
        elif resp.status_code == 404:
            return False 
        else:
            print(f"[Error] get_interface_config {if_name}: {resp.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"[Request Error] get_interface_config: {e}")
        return None

def create():

    if_name = f"Loopback66070276"
    

    if get_interface_config(if_name):
        return "Cannot create: Interface loopback 66070276"
    
    else:
        yangConfig = {
            "ietf-interfaces:interface": {
                "name": "Loopback66070276",
                "description": "Created by RESTCONF",
                "type": "iana-if-type:softwareLoopback",
                "enabled": True,
                "ietf-ip:ipv4": {
                    "address": [
                        {"ip": "172.2.76.1", "netmask": "255.255.255.0"}
                    ]
                },
                "ietf-ip:ipv6": {}
            }
        }

        api_url = f"{api_base}/interface={if_name}"
        resp = requests.put(
            api_url,
            data=json.dumps(yangConfig),
            auth=basicauth,
            headers=headers,
            verify=False
        )

        if 200 <= resp.status_code <= 299:
            return "Interface loopback 66070276 is created successfully"


def delete():

    if_name = f"Loopback66070276"

    if not get_interface_config(if_name):
        return "Cannot delete: Interface loopback 66070276"
    
    else:
        api_url = f"{api_base}/interface={if_name}"
        resp = requests.delete(
            api_url,
            auth=basicauth,
            headers=headers,
            verify=False
        )
        if 200 <= resp.status_code <= 299:
            return "Interface loopback 66070276 is deleted successfully"


def enable():
    if_name = f"Loopback66070276"
    if not get_interface_config(if_name):
        return "Cannot enable: Interface loopback 66070276"
    else:
        api_url = f"{api_base}/interface={if_name}"
        yangConfig = {"ietf-interfaces:interface": {"enabled": True}}
        resp = requests.patch(api_url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)
        if 200 <= resp.status_code <= 299:
            return "Interface loopback 66070276 is enabled successfully"


def disable():
    if_name = f"Loopback66070276"
    if not get_interface_config(if_name):
        return "Cannot enable: Interface loopback 66070276"
    else:
        api_url = f"{api_base}/interface={if_name}"
        yangConfig = {"ietf-interfaces:interface": {"enabled": False}}
        resp = requests.patch(api_url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)
        if 200 <= resp.status_code <= 299:
            return "Interface loopback 66070276 is shutdowned successfully"


def status():
    if_name = f"Loopback66070276"
    if not get_interface_config(if_name):
        return "No Interface loopback 66070276"
    else:

        api_url_status = f"https://{router_ip}/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback66070276"
        resp = requests.get(api_url_status, auth=basicauth, headers=headers, verify=False)

        if 200 <= resp.status_code <= 299:
            data = resp.json()
            admin_status = data["ietf-interfaces:interface"]["admin-status"]
            oper_status = data["ietf-interfaces:interface"]["oper-status"]
            if admin_status == "up" and oper_status == "up":
                return "Interface loopback 66070276 is enabled"
            elif admin_status == "down" and oper_status == "down":
                return "Interface loopback 66070276 is disabled"


    

