#!/bin/sh

if [ -d /etc/X11/xinit/xinitrc.d ] ; then
 for f in /etc/X11/xinit/xinitrc.d/?*.sh ; do
  [ -x "$f" ] && . "$f"
 done
 unset f
fi

[ -f ~/.xprofile ] && . ~/.xprofile

xrandr --auto
xrandr --dpi 96

# xrandr --setprovideroutputsource modesetting NVIDIA-0

xsetroot -cursor_name left_ptr &

# map super keys to trigger when used alone
xcape -e 'Super_L=Super_L|F1' &

# turn on numlock
numlockx on &

# enable natural scrolling & tapping on the touchpad
xinput set-prop "AlpsPS/2 ALPS GlidePoint" "libinput Natural Scrolling Enabled" 1
xinput set-prop "AlpsPS/2 ALPS GlidePoint" "libinput Tapping Enabled" 1

#################
# auto start
#################

# keybindings
exec sxhkd &

# compositor
picom --experimental-backends --backend glx -b &

# redshift
redshift -m randr &

# touchpad gestures
fusuma &

# network manager tray
nm-applet &

# bluetooth manager tray
# blueman-applet &

# authentication agent
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &

# notification daemon
dunst &

# discord
discord --start-minimized &

# window manager
exec bspwm
