#!/usr/bin/pypy3

import subprocess
import time

from pynput import mouse

try:
    while True:
        result = str(subprocess.run(["xset", "q"], capture_output=True).stdout)

        if result[result.index("Caps") + 13 : result.index("Caps") + 15] == "on":
            mouse.Controller().click(mouse.Button.left)

        time.sleep(0.05)

except KeyboardInterrupt:
    print("terminated\n")

except Exception as e:
    raise e
