from netmiko import ConnectHandler
from pprint import pprint


device_ip = "10.0.15.62"
username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_ios",
    "ip": device_ip,
    "username": username,
    "password": password,
    "conn_timeout": 20,
    "banner_timeout": 30
}


def gigabit_status():
    status_list = []
    
    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0
        
        result = ssh.send_command("show ip interface brief", use_textfsm=True)
        
        for status in result:

            if status["interface"].startswith("GigabitEthernet"):
            
                intf_status = status["status"]
                
                status_list.append(f'{status["interface"]} {intf_status}')
                

                if intf_status == "up":
                    up += 1
                elif intf_status == "down":
                    down += 1
                elif intf_status == "administratively down":
                    admin_down += 1

        ans = f'{", ".join(status_list)} -> {up} up, {down} down, {admin_down} administratively down'
        print(ans)
        return ans
