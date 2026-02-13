import json
from netmiko import ConnectHandler
from netmiko import (
    NetmikoAuthenticationException,
    NetmikoTimeoutException,
)


with open("MODULE 1/device.json") as f:
   devices = json.load(f)


vlan_ID = "60"
vlan_NAME = "MANGO"


for device in devices:
   print(f"\n     ============================================")
   print(f" Device: {device['name']} | Role: {device['role']} | IP: {device['connection']['host']}")
   print(f"    =============================================")
   if device['role'] != "access":
      print(f"This is NOT Access {device['role']} - Skipping...")
      continue
   else:   
      try:
         connection = ConnectHandler(**device['connection'])
         connection.enable()
         input_output = connection.send_command("sh vlan br")
         if vlan_ID in input_output:
            print(f"VLAN {vlan_ID} is Already Exits...")
            continue
         else:
            print(f"VLAN {vlan_ID} is Creating...")
            commands = [
               f"vlan {vlan_ID}",
               f"name {vlan_NAME}",
            ]         
            connection.send_config_set(commands)
            very = connection.send_command(f"sh vlan br | include {vlan_ID}")
            print(very)
            connection.disconnect()
      except NetmikoAuthenticationException:
         print("Authentication Is Failed....")
      except NetmikoTimeoutException:
         print("SSH TimeOut / Device is NOT Reachable...")

   
   