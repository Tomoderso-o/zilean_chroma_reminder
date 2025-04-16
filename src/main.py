import subprocess
import requests
import random
import time
import os
import sys


# random time between 0s and 2s. May help against Vanguard?
time_salt = random.randrange(0 , 200, 1) / 100

def get_reminder_list():
    filepath = get_resource_path('shop_reminder_list.txt')
    # create if not exists
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            f.write('Sugar Rush Zilean\n')
            f.write('Zilean\n')
    
    # open existing file
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # remove newlines and carriage returns
    reminder_items = []
    for line in lines:
        l = line.replace('\n', '').replace('\r', '')
        if l:
            reminder_items.append(l)
    return reminder_items


def get_app_dir():
    # gets the correct app directory, regardless if in dev or deployed
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(__file__)
    return base_path

def get_resource_path(filename):
    return os.path.join(get_app_dir(), filename)


# get Basic auth string, port and league directory
output = subprocess.Popen(
    [
        'powershell.exe', '-ExecutionPolicy', 'Bypass', '-File', get_resource_path("get_auth.ps1")
    ], 
    shell=True,  # without this a terminal window would open for a split second
    # allows capturing output
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
output.wait()
# output is provided using Write-Host, so it needs to be parsed accordingly
output_lines = output.stdout.read().decode().split('\n')
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
time.sleep(1 + time_salt)

get_active_stores_retries = 0
while True:
    try:
        # set active store, so get-active-stores is available
        set_store_response = requests.post(
            f'{host}/lol-nacho/v1/set-active-stores',
            headers=headers,
            data='{"request": "MYTHIC_SHOP"}',
            verify=False
        )
        
        # small delay because client needs time to change state
        time.sleep(1)

        # get-active-store
        get_store_response = requests.get(
            f'{host}/lol-nacho/v1/get-active-stores', 
            headers=headers, 
            verify=False,
        )

        # only check get_store_response status code, 
        # because set_store_response will always be 204 No Content.
        # Sometimes set_store_response will also just not work. So retry until get_active_store succeeds
        if get_store_response.status_code == 200:
            break
        else:
            # there would be an endpoint to check if the store is ready, but why not just use this?
            raise Exception('Store not ready')
    except Exception:
        if get_active_stores_retries > 20:
            sys.exit(1)
        else:
            get_active_stores_retries += 1
            time.sleep(2 + time_salt)

# convert reponse to string because it's sufficient and so no complex parsing is needed
mythic_shop = str(get_store_response.json())

# read local reminder list file
reminder_list = get_reminder_list()

# show toast for every reminder
for reminder in reminder_list:
    if reminder.lower() in mythic_shop.lower():
        # input args for toast
        app_display_name = 'Zilean Toasts'
        toast_text = '💖' if reminder == 'Sugar Rush Zilean' else random.choice('👀✨🔔🌟💫')
        toast_title = f'{reminder} ist im Mythic Shop!'
        image_path = get_resource_path("zilean_toast.png")
        expiration_in_mins = "30"
        # display the toast notification
        toast_notification = subprocess.Popen(
            [
                # call script
                'powershell.exe', '-ExecutionPolicy', 'Bypass', '-File', get_resource_path("toast_script.ps1"),
                # script inputs. Order matters
                app_display_name, toast_text, toast_title, image_path, expiration_in_mins
            ],
            shell=True,  # without this a terminal window would open for a split second
        )
        toast_notification.wait()
        time.sleep(1)