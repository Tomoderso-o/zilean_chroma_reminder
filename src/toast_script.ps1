$leagueDir = $args[0]
$toastText = $args[1]
$toastTitle = $args[2]

# Step 4: Show Windows Toast Notification
Add-Type -AssemblyName System.Windows.Forms 
$global:balloon = New-Object System.Windows.Forms.NotifyIcon
$path = (Get-Process -Id $pid).Path
#$path = Join-Path -Path $leagueDir -ChildPath "LeagueClientUx.exe"
$balloon.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon($path) 
$balloon.BalloonTipIcon = [System.Windows.Forms.ToolTipIcon]::Info
$balloon.BalloonTipText = $toastText
$balloon.BalloonTipTitle = $toastTitle 
$balloon.Visible = $true 
$balloon.ShowBalloonTip(5000)


Write-Host "Notification Sent!"