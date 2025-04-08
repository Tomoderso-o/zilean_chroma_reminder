# Step 1: Wait for League Client
$processName = "LeagueClientUx"
#Write-Host "Waiting for League Client to launch..."
while ($true) {
    $process = Get-Process -Name $processName -ErrorAction SilentlyContinue
    if ($process) {
        # Get the executable's full path
        $leaguePath = $process.Path
        # Extract the directory from the full path
        $leagueDir = Split-Path -Path $leaguePath -Parent
        #Write-Host "League of Legends is installed at: $leagueDir"
        break
    }
    Start-Sleep -Seconds 5
}

# Step 2: Read LCU API Credentials
$lockfilePath = Join-Path -Path $leagueDir -ChildPath "lockfile"
while (-not (Test-Path $lockfilePath)) {
    Start-Sleep -Seconds 5
}

$lockfileContent = Get-Content $lockfilePath
$lockfileParts = $lockfileContent -split ':'
$port = $lockfileParts[2]
$password = $lockfileParts[3]

$encodedAuth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("riot:$password"))

Write-Host $port
Write-Host $encodedAuth