import subprocess
import requests
import random
import time
import os
import sys


def get_reminder_list():
    filepath = get_resource_path('shop_reminder_list.txt')
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            f.write('')
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
    # remove newlines and carriege returns
    reminder_items = []
    for line in lines:
        l = line.replace('\n', '').replace('\r', '')
        if l:
            reminder_items.append(l)
    return reminder_items


def get_app_dir():
    if getattr(sys, 'frozen', False):
        dirname = os.path.dirname(sys.executable)
        base_path = os.path.join(dirname, '_internal')
    else:
        base_path = os.path.dirname(__file__)
    return base_path

def get_resource_path(filename):
    return os.path.join(get_app_dir(), filename)


# get Basic auth string, port and league directory
output = subprocess.Popen(
    [
        'powershell.exe', 
        '-ExecutionPolicy',
        'Bypass',
        '-File',
        get_resource_path("get_auth.ps1")
    ], 
    shell=True, 
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
output.wait()
output_lines = output.stdout.read().decode().split('\n')
print(output_lines)
print(output.stderr.read())
port = output_lines[0].strip()
encoded_auth = output_lines[1].strip()
league_dir = output_lines[2].strip()

# prepare lcu requests
headers = {
    "Authorization" : f'Basic {encoded_auth}', 
    'Content-Type': 'application/json'
}
host = f'https://127.0.0.1:{port}' 

# Wait for the client
random_time = random.randrange(0 , 200, 1) / 100
time.sleep(1 + random_time)

while True:
    try:
        # set active store, so get-active-stores is available
        r = requests.post(
            f'{host}/lol-nacho/v1/set-active-stores',
            headers=headers,
            data='{"request": "MYTHIC_SHOP"}',
            verify=False
        )
        print(r.status_code)
        break
    except Exception:
        time.sleep(2 + random_time)

time.sleep(2)
while True:
    try:
        # set active store, so get-active-stores is available
        response = requests.get(
            f'{host}/lol-nacho/v1/get-active-stores', 
            headers=headers, 
            verify=False
        )
        if not response.ok:
            raise Exception('Store not ready')
        else:
            break
    except Exception:
        time.sleep(2 + random_time)

mythic_shop = str(response.json())

reminder_list = get_reminder_list()

for reminder in reminder_list:
    if reminder.lower() in mythic_shop.lower():
        with open(get_resource_path(reminder + '.txt'), 'w') as f:
            f.writelines([
                _ + '\n' for _ in  
                [
                '|| Toast Script Path',
                get_resource_path("toast_script.ps1"), 
                '|| Reminder',
                reminder, 
                '|| Reminder List',
                str(reminder_list), 
                '|| Mythic Shop',
                mythic_shop
            ]])
        
        app_display_name = 'Zilean Toasts'
        toast_text = '💖'
        toast_title = f'{reminder} ist im Mythic Shop!'
        image_path = get_resource_path("zilean_toast.png")
        expiration_in_mins = "10"
        # display the toast notification
        toast_notification = subprocess.Popen(
            [
                # call script
                'powershell.exe', '-ExecutionPolicy', 'Bypass', '-File', get_resource_path("toast_script.ps1"),
                # script inputs. Order matters
                app_display_name, toast_text, toast_title, image_path, expiration_in_mins
            ],
            shell=True,
        )
        toast_notification.wait()
        time.sleep(1)