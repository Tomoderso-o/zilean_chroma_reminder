Lockfile liegt hier

`"D:\Riot Games\League of Legends\lockfile"`

Format ist

`Process Name : Process ID : Port : Password : Protocol`

Basic auth bei Anfrage in Header hinzufügen:
`Authorization: Basic <base 64 encoded -> riot:password>`

Geben Mythic Shop zurück

`curl -H "Authorization: Basic <encoded>"  --insecure https://127.0.0.1:50956/lol-nacho/v1/get-active-stores`

`curl -H "Authorization: Basic <encoded>"  --insecure https://127.0.0.1:50956/lol-nacho/v1/get-active-store-catalog`

Nacho store

https://lcu.kebs.dev/#tag-Plugin%20lol-nacho

Blog
https://hextechdocs.dev/getting-started-with-the-lcu-api/





Store setzen
`curl -H "Authorization: Basic <encoded>" -H 'Content-Type: application/json'  --insecure "https://127.0.0.1:59048/lol-nacho/v1/set-active-stores/" -X POST -d '{"request": "MYTHIC_SHOP"}'`
dann abrufen

`curl -H "Authorization: Basic <encoded>" -H 'Content-Type: application/json'  --insecure "https://127.0.0.1:59048/lol-nacho/v1/get-active-stores"`