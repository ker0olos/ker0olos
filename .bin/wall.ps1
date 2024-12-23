param (
    [string]$Arg1,
    [string]$Arg2,
    [string]$Arg3
)

# Create directories/files
New-Item -ItemType Directory -Path "$env:USERPROFILE\Pictures\.wall" -Force | Out-Null
New-Item -ItemType File -Path "$env:USERPROFILE\Pictures\.wall\default" -Force | Out-Null
New-Item -ItemType Directory -Path "$env:USERPROFILE\Pictures\.wall\.bookmarks" -Force | Out-Null

function Set-Wallpaper {
    param([string]$imagePath)
    # Basic approach to set wallpaper via SystemParametersInfo
    Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class Wallpaper {
    [DllImport("user32.dll", CharSet=CharSet.Auto)]
    public static extern int SystemParametersInfo (int uAction, int uParam, string lpvParam, int fuWinIni);
}
"@
    [Wallpaper]::SystemParametersInfo(20, 0, $imagePath, 0x1)
}

if ($Arg1 -eq "-u") {
    Set-Wallpaper $Arg2
    $cmd = "Set-Wallpaper `"$Arg2`""
    $cmd | Out-File "$env:USERPROFILE\Pictures\.wall\default"
    Write-Host "Wallpaper updated: $Arg2"
}
elseif ([string]::IsNullOrEmpty($Arg1)) {
    Invoke-Expression (Get-Content "$env:USERPROFILE\Pictures\.wall\default" | Out-String)
}
else {
    $bookmark = Join-Path "$env:USERPROFILE\Pictures\.wall\.bookmarks" $Arg1
    if (Test-Path $bookmark) {
        Copy-Item $bookmark "$env:USERPROFILE\Pictures\.wall\default" -Force
        Invoke-Expression (Get-Content "$env:USERPROFILE\Pictures\.wall\default" | Out-String)
    }
    else {
        Copy-Item "$env:USERPROFILE\Pictures\.wall\default" $bookmark -Force
        Write-Host "Bookmarked: $Arg1"
    }
}