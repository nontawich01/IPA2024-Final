#######################################################################################
# Yourname:
# Your student ID:
# Your GitHub Repo: 

#######################################################################################
# 1. Import libraries for API requests, JSON formatting, time, os, (restconf_final or netconf_final), netmiko_final, and ansible_final.

import requests
import json
import time
import os
import restconf_final
import netmiko_final
from requests_toolbelt.multipart.encoder import MultipartEncoder
import ansible_final
#######################################################################################
# 2. Assign the Webex access token to the variable ACCESS_TOKEN using environment variables.

ACCESS_TOKEN = os.environ.get("WEBEX_ACCESS_TOKEN")
ROOM_ID =os.environ.get("ROOM_ID")
#######################################################################################
# 3. Prepare parameters get the latest message for messages API.

# Defines a variable that will hold the roomId
roomIdToGetMessages = (
    ROOM_ID
)

while True:
    # always add 1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)

    # the Webex Teams GET parameters
    #  "roomId" is the ID of the selected room
    #  "max": 1  limits to get only the very last message in the room
    getParameters = {"roomId": roomIdToGetMessages, "max": 1}

    # the Webex Teams HTTP header, including the Authoriztion
    getHTTPHeader = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# 4. Provide the URL to the Webex Teams messages API, and extract location from the received message.
    
    # Send a GET request to the Webex Teams messages API.
    # - Use the GetParameters to get only the latest message.
    # - Store the message in the "r" variable.
    r = requests.get(
        "https://webexapis.com/v1/messages",
        params=getParameters,
        headers=getHTTPHeader,
    )
    # verify if the retuned HTTP status code is 200/OK
    if not r.status_code == 200:
        raise Exception(
            "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
        )

    # get the JSON formatted returned data
    json_data = r.json()

    # check if there are any messages in the "items" array
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")

    # store the array of messages
    messages = json_data["items"]
    
    # store the text of the first message in the array
    message = messages[0]["text"]
    print("Received message: " + message)

    # check if the text of the message starts with the magic character "/" followed by your studentID and a space and followed by a command name
    #  e.g.  "/66070123 create"
    if message.startswith("/66070276 "):
        command = message.split(" ")[1].strip()
        print("Command:", command)

# 5. Complete the logic for each command

        if command == "create":
            responseMessage = restconf_final.create()
        elif command == "delete":
            responseMessage = restconf_final.delete()
        elif command == "enable":
            responseMessage = restconf_final.enable()
        elif command == "disable":
            responseMessage = restconf_final.disable()
        elif command == "status":
            responseMessage = restconf_final.status()
        elif command == "gigabit_status":
            responseMessage = netmiko_final.gigabit_status()
        elif command == "showrun":
            # เรียกใช้ฟังก์ชันจาก ansible_final.py
            status, filename = ansible_final.showrun()
            
            # ตรวจสอบผลลัพธ์
            if status == 'ok' and filename:
                responseMessage = f"Attached is the running config: {filename}"
                
                # เตรียมข้อมูลสำหรับส่งไฟล์โดยใช้ MultipartEncoder
                postData = MultipartEncoder({
                    "roomId": roomIdToGetMessages,
                    "files": (filename, open(filename, 'rb'), 'text/plain'),
                    "text": f"{filename}"
                })
                
                # Header สำหรับ Multipart ต้องระบุ Content-Type ที่ถูกต้อง
                postHTTPHeader = {
                    "Authorization": f"Bearer {ACCESS_TOKEN}",
                    "Content-Type": postData.content_type
                }
            else:
                # ถ้าล้มเหลว, status จะเป็นข้อความ Error
                responseMessage = status 
        else:
            responseMessage = "Error: No command or unknown command"
        
# 6. Complete the code to post the message to the Webex Teams room.
        if command == "showrun" and postData:
            rp = requests.post(
                "https://webexapis.com/v1/messages",
                headers=postHTTPHeader,
                data=postData
            )
        else:
            data = {"roomId": roomIdToGetMessages, "text": responseMessage}
            rp = requests.post(
                "https://webexapis.com/v1/messages",
                headers=getHTTPHeader,
                data=json.dumps(data)
            )

        if rp.status_code == 200:
            print("Message sent to Webex successfully")
        else:
            print(f"Error sending message: {rp.status_code}")
        # The Webex Teams POST JSON data for command showrun
        # - "roomId" is is ID of the selected room
        # - "text": is always "show running config"
        # - "files": is a tuple of filename, fileobject, and filetype.

        # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
        
        # Prepare postData and HTTPHeaders for command showrun
        # Need to attach file if responseMessage is 'ok'; 
        # Read Send a Message with Attachments Local File Attachments
        # https://developer.webex.com/docs/basics for more detail

        # if command == "showrun" and responseMessage == 'ok':
        #     filename = "<!!!REPLACEME with show run filename and path!!!>"
        #     fileobject = <!!!REPLACEME with open file!!!>
        #     filetype = "<!!!REPLACEME with Content-type of the file!!!>"
        #     postData = {
        #         "roomId": <!!!REPLACEME!!!>,
        #         "text": "show running config",
        #         "files": (<!!!REPLACEME!!!>, <!!!REPLACEME!!!>, <!!!REPLACEME!!!>),
        #     }
        #     postData = MultipartEncoder(<!!!REPLACEME!!!>)
        #     HTTPHeaders = {
        #     "Authorization": ACCESS_TOKEN,
        #     "Content-Type": <!!!REPLACEME with postData Content-Type!!!>,
        #     }
        # # other commands only send text, or no attached file.
        # else:
        #     postData = {"roomId": <!!!REPLACEME!!!>, "text": <!!!REPLACEME!!!>}
        #     postData = json.dumps(postData)

        #     # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
        #     HTTPHeaders = {"Authorization": <!!!REPLACEME!!!>, "Content-Type": <!!!REPLACEME!!!>}   

        # # Post the call to the Webex Teams message API.
        # r = requests.post(
        #     "<!!!REPLACEME with URL of Webex Teams Messages API!!!>",
        #     data=<!!!REPLACEME!!!>,
        #     headers=<!!!REPLACEME!!!>,
        # )
        # if not r.status_code == 200:
        #     raise Exception(
        #         "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
        #     )
