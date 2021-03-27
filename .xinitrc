#!/bin/sh

# userresources=$HOME/.Xresources
# usermodmap=$HOME/.Xmodmap

sysresources=/etc/X11/xinit/.Xresources
sysmodmap=/etc/X11/xinit/.Xmodmap

# merge in defaults and keymaps

if [ -f $sysresources ]; then
    xrdb -merge $sysresources
fi

if [ -f $sysmodmap ]; then
    xmodmap $sysmodmap
fi

# if [ -f "$userresources" ]; then
#     xrdb -merge "$userresources"
# fi

# if [ -f "$usermodmap" ]; then
#     xmodmap "$usermodmap"
# fi

if [ -d /etc/X11/xinit/xinitrc.d ] ; then
 for f in /etc/X11/xinit/xinitrc.d/?*.sh ; do
  [ -x "$f" ] && . "$f"
 done
 unset f
fi

[ -f ~/.xprofile ] && . ~/.xprofile

eval $(/usr/bin/gnome-keyring-daemon --start --components=pkcs11,secrets,ssh)

export SSH_AUTH_SOCK

xsetroot -cursor_name left_ptr &

# map super keys to trigger when used alone
xcape -e 'Super_L=Super_L|F1' &
# keybindings
exec sxhkd &
# compositor
picom --experimental-backends --backend glx -b &
# redlight
redshift &
# pamac update notifier tray
pamac-tray &
# network manager tray
nm-applet &
# battery level notifications
batsignal -b -w 20 -c 10 -d 5 -f 99 &
# start spotifyd service
spotifyd &
# authentication agent
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
# notification daemon 
dunst &
# window manager
exec bspwm