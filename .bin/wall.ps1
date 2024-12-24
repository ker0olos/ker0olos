param (
    [string]$Arg1,
    [string]$Arg2
)

New-Item -ItemType Directory -Path "$env:USERPROFILE\Pictures\.wall" -Force | Out-Null

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

Set-Wallpaper $Arg1
