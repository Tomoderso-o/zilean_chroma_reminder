
# Step 4: Show Windows Toast Notification
Add-Type -AssemblyName System.Windows.Forms 
$global:balloon = New-Object System.Windows.Forms.NotifyIcon
$path = (Get-Process -Id $pid).Path
#$path = Join-Path -Path $leagueDir -ChildPath "LeagueClient.exe"
$balloon.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon($path) 
$balloon.BalloonTipIcon = [System.Windows.Forms.ToolTipIcon]::Info
$balloon.BalloonTipText = 'Zilean gefunden!'
$balloon.BalloonTipTitle = "Zilean Chroma" 
$balloon.Visible = $true 
$balloon.ShowBalloonTip(5000)


Write-Host "Notification Sent!"