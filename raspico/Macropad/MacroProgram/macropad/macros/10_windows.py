# SPDX-FileCopyrightText: 2021 Emma Humphries for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# MACROPAD Hotkeys Template

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values

app = {                          # REQUIRED dict, must be named 'app'
    'name' : 'Windows', # Application name
    'macros' : [                 # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x32ffff, 'Word',  [Keycode.CONTROL, Keycode.GUI, Keycode.LEFT_ALT, Keycode.SHIFT, 'w']),
        (0x00ff00, 'Excel', [Keycode.CONTROL, Keycode.GUI, Keycode.LEFT_ALT, Keycode.SHIFT, 'x']),
        (0xff00ff, 'Teams', [Keycode.CONTROL, Keycode.GUI, Keycode.LEFT_ALT, Keycode.SHIFT, 't']),
        # 2nd row ----------
        (0xfdf5e6, 'Files',  [Keycode.GUI, 'e']),
        (0xff0000, 'Snip',   [Keycode.GUI, Keycode.SHIFT, 's']),
        (0x00ffff, 'Desktop',[Keycode.GUI, 'd']),
        # 3rd row ----------
        (0x00ff28, 'TaskMgr', [Keycode.CONTROL, Keycode.SHIFT, Keycode.ESCAPE]),
        (0xf25aff, 'Emoji', [Keycode.GUI, '.']),
        (0xff6400, 'Panes', [Keycode.GUI, Keycode.TAB]),
        # 4th row ----------
        (0xff0014, 'Calc', [Keycode.GUI, 'r', -Keycode.GUI, 0.2, 'calc', 0.1, Keycode.ENTER]),
        (0xffff00, 'WSL', [Keycode.GUI, 'r', -Keycode.GUI, 0.2, 'wsl', 0.1, Keycode.ENTER]),
        (0x0000ff, 'PS', [Keycode.GUI, 'r', -Keycode.GUI, 0.2, 'powershell', 0.1, Keycode.ENTER]),
        # Encoder button ---
        (0x000000, '', [])
    ]
}
