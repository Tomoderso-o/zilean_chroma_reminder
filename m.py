import subprocess
import requests


auth_script = "./get_auth.ps1"
output = subprocess.Popen(
    [
    'powershell.exe', auth_script
    ], 
    shell=True, 
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
output_lines = output.stdout.read().decode().split('\n')
port = output_lines[0].strip()
encoded_auth = output_lines[1].strip()

headers = {
    "Authorization" : f'Basic {encoded_auth}', 
    'Content-Type': 'application/json'
}
host = f'https://127.0.0.1:{port}' 

r = requests.post(
    f'{host}/lol-nacho/v1/set-active-stores',
    headers=headers,
    data='{"request": "MYTHIC_SHOP"}',
    verify=False
)
response = requests.get(
    f'{host}/lol-nacho/v1/get-active-stores', 
    headers=headers, 
    verify=False
)
print(response)
print(response.json())
if 'Ekko' in str(response.json()):
    print('Ekko found!')
    subprocess.Popen(
        [
        'powershell.exe', './toast_script.ps1'
        ], 
        shell=True,
    )