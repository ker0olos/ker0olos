#!/usr/bin/env bash

# CONFIGURATION
LOCATION=0
YOFFSET=0
XOFFSET=0
WIDTH=12
WIDTH_WIDE=24
THEME=solarized

# Color Settings of Icon shown in Polybar
COLOR_DISCONNECTED='#707070'
COLOR_NEWDEVICE='#4aff56'

COLOR_BATTERY_10='#e31e1e'
COLOR_BATTERY_20='#e3b039'
COLOR_BATTERY_100='#1eff00'

# Icons shown in Polybar
ICON_PHONE='󰄜'
ICON_CHARGING='󱎗'

SEPERATOR='|'

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

show_devices (){
  IFS=$','
  devices=""

  for device in $(qdbus --literal org.kde.kdeconnect /modules/kdeconnect org.kde.kdeconnect.daemon.devices); do

    deviceid=$(echo "$device" | awk -F'["|"]' '{print $2}')
    devicename=$(qdbus org.kde.kdeconnect "/modules/kdeconnect/devices/$deviceid" org.kde.kdeconnect.device.name)
    devicetype=$(qdbus org.kde.kdeconnect "/modules/kdeconnect/devices/$deviceid" org.kde.kdeconnect.device.type)
    isreach="$(qdbus org.kde.kdeconnect "/modules/kdeconnect/devices/$deviceid" org.kde.kdeconnect.device.isReachable)"
    istrust="$(qdbus org.kde.kdeconnect "/modules/kdeconnect/devices/$deviceid" org.kde.kdeconnect.device.isTrusted)"
    
    if [ "$isreach" = "true" ] && [ "$istrust" = "true" ]
    then
        battery="$(qdbus org.kde.kdeconnect "/modules/kdeconnect/devices/$deviceid/battery" org.kde.kdeconnect.device.battery.charge)"
        isCharging="$(qdbus org.kde.kdeconnect "/modules/kdeconnect/devices/$deviceid/battery" org.kde.kdeconnect.device.battery.isCharging)"
        
        icon=$(get_icon "$battery" "$isCharging")
        devices+="%{A1:$DIR/kdeconnect.sh -n '$devicename' -i $deviceid -b $battery -m:}$icon%{A}$SEPERATOR"
    elif [ "$isreach" = "false" ] && [ "$istrust" = "true" ]
    then
        devices+="$(get_icon -1)$SEPERATOR"
    else
        haspairing="$(qdbus org.kde.kdeconnect "/modules/kdeconnect/devices/$deviceid" org.kde.kdeconnect.device.hasPairingRequests)"

        if [ "$haspairing" = "true" ]
        then
          show_pmenu2 "$devicename" "$deviceid"
        fi

        icon=$(get_icon -2)
        devices+="%{A1:$DIR/kdeconnect.sh -n $devicename -i $deviceid -p:}$icon%{A}$SEPERATOR"
    fi
  done

  echo "${devices::-1}"
}

show_menu () {
  menu="$(rofi -sep "|" -dmenu -i -p "$DEV_NAME" -location $LOCATION -yoffset $YOFFSET -xoffset $XOFFSET -theme $THEME -width $WIDTH -hide-scrollbar -line-padding 4 -padding 20 -lines 5 <<< "Battery: $DEV_BATTERY%|Ping|Find Device|Send File|Browse Files|Settings|Unpair")"
  
  case "$menu" in
    *'Ping') qdbus org.kde.kdeconnect "/modules/kdeconnect/devices/$DEV_ID/ping" org.kde.kdeconnect.device.ping.sendPing ;;
    *'Find Device') qdbus org.kde.kdeconnect "/modules/kdeconnect/devices/$DEV_ID/findmyphone" org.kde.kdeconnect.device.findmyphone.ring ;;
    *'Send File') qdbus org.kde.kdeconnect "/modules/kdeconnect/devices/$DEV_ID/share" org.kde.kdeconnect.device.share.shareUrl "file://$(zenity --file-selection)" ;;
    *'Browse Files')
      if "$(qdbus --literal org.kde.kdeconnect "/modules/kdeconnect/devices/$DEV_ID/sftp" org.kde.kdeconnect.device.sftp.isMounted)" == "false"; then
        qdbus org.kde.kdeconnect "/modules/kdeconnect/devices/$DEV_ID/sftp" org.kde.kdeconnect.device.sftp.mount
      fi

      qdbus org.kde.kdeconnect "/modules/kdeconnect/devices/$DEV_ID/sftp" org.kde.kdeconnect.device.sftp.startBrowsing
      ;;
    *'Settings' ) kdeconnect-settings ;;
    *'Unpair' ) qdbus org.kde.kdeconnect "/modules/kdeconnect/devices/$DEV_ID" org.kde.kdeconnect.device.unpair
  esac
}

show_pmenu () {
  menu="$(rofi -sep "|" -dmenu -i -p "$DEV_NAME" -location $LOCATION -yoffset $YOFFSET -xoffset $XOFFSET -theme $THEME -width $WIDTH -hide-scrollbar -line-padding 1 -padding 20 -lines 1<<<"Pair Device")"
    case "$menu" in
      *'Pair Device') qdbus org.kde.kdeconnect "/modules/kdeconnect/devices/$DEV_ID" org.kde.kdeconnect.device.requestPair
    esac
}

show_pmenu2 () {
  menu="$(rofi -sep "|" -dmenu -i -p "$1 has sent a pairing request" -location $LOCATION -yoffset $YOFFSET -xoffset $XOFFSET -theme $THEME -width $WIDTH_WIDE -hide-scrollbar -line-padding 4 -padding 20 -lines 2 <<< "Accept|Reject")"
  
  case "$menu" in
    *'Accept') qdbus org.kde.kdeconnect "/modules/kdeconnect/devices/$2" org.kde.kdeconnect.device.acceptPairing ;;
    *) qdbus org.kde.kdeconnect "/modules/kdeconnect/devices/$2" org.kde.kdeconnect.device.rejectPairing
  esac
}

get_icon () {
  icon=$ICON_PHONE

  if [ "$2" = "true" ]
  then
      icon="$ICON_CHARGING"
  fi

  case $1 in
    "-1") ICON="%{F$COLOR_DISCONNECTED}%{T3}$icon%{T-}%{F-}" ;;
    "-2") ICON="%{F$COLOR_NEWDEVICE}%{T3}$icon%{T-}%{F-}" ;;
    2*)   ICON="%{F$COLOR_BATTERY_20}%{T3}$icon%{T-}%{F-}" ;;
    3*)   ICON="%{T3}$icon%{T-}" ;;
    4*)   ICON="%{T3}$icon%{T-}" ;;
    5*)   ICON="%{T3}$icon%{T-}" ;;
    6*)   ICON="%{T3}$icon%{T-}" ;;
    7*)   ICON="%{T3}$icon%{T-}" ;;
    8*)   ICON="%{T3}$icon%{T-}" ;;
    9*|100)  ICON="%{F$COLOR_BATTERY_100}%{T3}$icon%{T-}%{F-}" ;;
    *)       ICON="%{F$COLOR_BATTERY_10}%{T3}$icon%{T-}%{F-}" ;;
  esac

  echo $ICON
}

unset DEV_ID DEV_NAME DEV_BATTERY

while getopts 'di:n:b:mp' c
do
  case $c in
    d) show_devices ;;
    i) DEV_ID=$OPTARG ;;
    n) DEV_NAME=$OPTARG ;;
    b) DEV_BATTERY=$OPTARG ;;
    m) show_menu ;;
    p) show_pmenu ;;
  esac
done
