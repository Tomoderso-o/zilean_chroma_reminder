﻿# Find the running League Client process



# Step 1: Wait for League Client
$processName = "LeagueClientUx"
Write-Host "Waiting for League Client to launch..."
while ($true) {
    $process = Get-Process -Name $processName -ErrorAction SilentlyContinue
    if ($process) {
        # Get the executable's full path
        $leaguePath = $process.Path
        # Extract the directory from the full path
        $leagueDir = Split-Path -Path $leaguePath -Parent
        Write-Host "League of Legends is installed at: $leagueDir"
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
$authHeader = @{ Authorization = "Basic $encodedAuth" }

Write-Host "LCU API detected at port $port"

# Step 3: Monitor LCU API for Champ Select
$lcuEndpoint = "https://127.0.0.1:$port/lol-nacho/v1/get-active-stores"


# Disable SSL certificate validation for this session
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }

while ($true) {
    #try {
        Write-Host $encodedAuth
        $response = Invoke-RestMethod -Uri $lcuEndpoint -Headers $authHeader -Method "Get"
        
        if($response) {
            Write-Host "Response"
            break
        }

        if ($response -like "*Zilean*") {
            Write-Host "Found Zilean"
            break
        }
    #} catch {
    #    Write-Host "LCU API not available. Retrying..."
    #}
    Start-Sleep -Seconds 5
}
Invoke-RestMethod -
# Step 4: Show Windows Toast Notification
Add-Type -AssemblyName System.Windows.Forms 
$global:balloon = New-Object System.Windows.Forms.NotifyIcon
$path = (Get-Process -Id $pid).Path
$balloon.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon($path) 
$balloon.BalloonTipIcon = [System.Windows.Forms.ToolTipIcon]::Warning 
$balloon.BalloonTipText = 'Test'
$balloon.BalloonTipTitle = "Test" 
$balloon.Visible = $true 
$balloon.ShowBalloonTip(5000)


Write-Host "Notification Sent!"