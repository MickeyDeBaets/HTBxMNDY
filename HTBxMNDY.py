import requests
import json
import base64
import time


htb_base_url = "https://www.hackthebox.eu/api/v4/"
htb_access_token = ""
htb_machines_dict = {}
htb_email = ".....@......com"
htb_password = "******"

mndy_access_token = "ey......."
mndy_api_url = "https://api.monday.com/v2"
mndy_tasks = []


# Get access token with email and password
def htb_get_access_token():       
    payload = json.dumps({"email": htb_email, "password": htb_password})
    headers = {
    'User-Agent': 'htb-api/0.4.1',  
    'Content-Type': 'application/json'
    }
    r = requests.post(htb_base_url + "login", headers=headers, data=payload)
    data = r.json()
    htb_access_token = data['message']['access_token']
    return htb_access_token


# List active machines
def htb_list_machines():
    headers = {
    'User-Agent': 'htb-api/0.4.1',  
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + htb_access_token
    }
    r = requests.get(htb_base_url + "machine/list", headers=headers)
    data = r.json()
    return data['info']


# List current tasks
def mnday_get_tasks():
    query = """{
        boards(
            ids: 1425539705) {
                items {name}
                }
            }"""
    headers = { 
    'Content-Type': 'application/json',
    'Authorization': mndy_access_token
    }
    r = requests.get(mndy_api_url, headers=headers, json={'query': query})
    data = r.json()
    return data['data']['boards'][0]['items']
    


# Create new task for new machines
def mndy_new_task(x, machines, tasks):
    if x not in tasks and (machines[i]['difficulty'] == "Easy" or machines[i]['difficulty'] == "Medium"):
        name = x
        priority = ""
        difficulty = ""
        os = ""
        
        if machines[i]['os'] == "Linux":
            os = '{\\\"labels\\\":[\\\"Linux\\\"]}'
        elif machines[i]['os'] == "Windows":
            os = '{\\\"labels\\\":[\\\"Windows\\\"]}'
        else:
            os = '{\\\"labels\\\":[\\\"Other\\\"]}'

        if machines[i]['difficulty'] == "Easy":
            priority = '{\\\"label\\\":\\\"P1\\\"}'
            difficulty = '{\\\"label\\\":\\\"Easy\\\"}'
        else:
            priority = '{\\\"label\\\":\\\"P3\\\"}'
            difficulty = '{\\\"label\\\":\\\"Medium\\\"}'

        mndy_json_data = f"""mutation {{create_item(board_id: 1425539705, item_name: "{name}", column_values: "{{\\\"status_1\\\" : {priority}, \\\"difficulty\\\" : {difficulty}, \\\"dropdown_1\\\" : {os}, \\\"tags8\\\" : {{\\\"tag_ids\\\":[10472449]}}}}" ) {{id}}}}"""
        headers = headers = { 
        'Content-Type': 'application/json',
        'Authorization': mndy_access_token
        }
        r = requests.post(mndy_api_url, headers=headers, json={'query': mndy_json_data})


htb_access_token = htb_get_access_token()
htb_machines_list = htb_list_machines()
mndy_tasks_list = mnday_get_tasks()

for i in htb_machines_list:
    if i['name'] not in htb_machines_dict:
        htb_machines_dict[i['name']] = {'os' : i['os'], 'difficulty' : i['difficultyText']}

for i in mndy_tasks_list:
    if i['name'] not in mndy_tasks:
        mndy_tasks.append(i['name'])

for i in htb_machines_dict:
    mndy_new_task(i, htb_machines_dict, mndy_tasks)
