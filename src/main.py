import subprocess
import requests
import time
import os
import sys
# if sys.platform == "win32":
#     import ctypes
#     ctypes.windll.kernel32.SetDllDirectoryW(None)

def get_resource_path(filename):
    if getattr(sys, 'frozen', False):
        dirname = os.path.dirname(sys.executable)
        base_path = os.path.join(dirname, '_internal')
    else:
        base_path = os.path.dirname(__file__)
        
    return f'&"{os.path.join(base_path, filename)}"'

# get Basic auth string, port and league directory
auth_script = get_resource_path("get_auth.ps1")
print(auth_script)
output = subprocess.Popen(
    [
    'powershell.exe', auth_script
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

while True:
    try:
        # set active store, so get-active-stores is available
        r = requests.post(
            f'{host}/lol-nacho/v1/set-active-stores',
            headers=headers,
            data='{"request": "MYTHIC_SHOP"}',
            verify=False
        )
        break
    except Exception:
        time.sleep(5)

# get mythic shop
response = requests.get(
    f'{host}/lol-nacho/v1/get-active-stores', 
    headers=headers, 
    verify=False
)
mythic_shop = str(response.json())

if True:
#if 'Zilean' in mythic_shop:
    subprocess.Popen(
        [
        'powershell.exe', 
        get_resource_path('toast_script.ps1'), 
        f"'{league_dir}'",
        "'Zilean ist im Shop!'",
        "'Mythic Shop'"
        ], 
        shell=True,
    )
