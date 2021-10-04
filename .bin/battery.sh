PERCENTAGE=$(cat /sys/class/power_supply/BAT0/capacity)

LOW_BATTERY=20

function check {

  if [ "$PERCENTAGE" -lt "$LOW_BATTERY" ]; then
    dunstify -r 500 -a "Warning:" "Low Battery ($PERCENTAGE%)"
    echo "Warning: Low Battery ($PERCENTAGE%)"
  else
    echo "BAT0: $PERCENTAGE%"
  fi

  sleep 1
  check
}

check