$argAppDisplayName = $args[0]
$argToastText = $args[1]
$argToastTitle = $args[2]
$argImgPath = $args[3]
$argExpirationInMins = $args[4]

function Show-Notification {
    [cmdletbinding()]
    Param (
        [string]
        $ToastTitle,
        [string]
        $ToastText,
        [string]
        $ImgPath,
        [string]
        $appDisplayName,
        [int]
        $expirationInMins
    )

    [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
    $Template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastImageAndText02)

    $RawXml = [xml] $Template.GetXml()
    # allows toast to show on screen, when do not disturb is on
    # https://learn.microsoft.com/en-us/uwp/schemas/tiles/toastschema/element-toast
    $RawXml.toast.SetAttribute("scenario", "urgent")
    ($RawXml.toast.visual.binding.text| Where-Object {$_.id -eq "1"}).AppendChild($RawXml.CreateTextNode($ToastTitle)) > $null
    ($RawXml.toast.visual.binding.text| Where-Object {$_.id -eq "2"}).AppendChild($RawXml.CreateTextNode($ToastText)) > $null

    # Resolve the image path to a URI
    if (-not [string]::IsNullOrEmpty($ImgPath)) {
        try {
            $ResolvedPath = (Get-Item $ImgPath).FullName
            $ImageUri = "file:///$($ResolvedPath -replace '\\', '/')"
        } catch {
            Write-Host "Invalid image path: $ImgPath" -ForegroundColor Red
            return
        }
    } else {
        $ImageUri = ""
    }

    # Set the image source
    $ImageNode = $RawXml.toast.visual.binding.image | Where-Object { $_.id -eq "1" }
    $ImageNode.SetAttribute("src", $ImageUri)
    $ImageNode.SetAttribute("alt", "Toast Image")
    $ImageNode.SetAttribute("hint-crop", "circle")

    $SerializedXml = New-Object Windows.Data.Xml.Dom.XmlDocument
    $SerializedXml.LoadXml($RawXml.OuterXml)

    $Toast = [Windows.UI.Notifications.ToastNotification]::new($SerializedXml)

    $Toast.ExpirationTime = [DateTimeOffset]::Now.AddMinutes($expirationInMins)

    $Notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($appDisplayName)
    $Notifier.Show($Toast);
}

Show-Notification -ToastTitle "$argToastTitle" -ToastText "$argToastText" -ImgPath "$argImgPath" -appDisplayName "$argAppDisplayName" -expirationInMins $argExpirationInMins