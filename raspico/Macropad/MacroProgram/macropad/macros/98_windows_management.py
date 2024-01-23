# SPDX-FileCopyrightText: 2021 Emma Humphries for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# MACROPAD Hotkeys Template

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values

app = {                             # REQUIRED dict, must be named 'app'
    'name' : 'Windows Admin',       # Application name
    'macros' : [                    # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x0000ff, 'PS', [Keycode.GUI, 'r', -Keycode.GUI, 0.2, 'powershell', 0.1, Keycode.ENTER]),
        (0x32ffff, 'Remote Desk', [Keycode.GUI, 'r', -Keycode.GUI, 0.2, 'mstsc', 0.1, Keycode.ENTER]),
        (0x00ff00, 'CMD',  [Keycode.GUI, 'r', -Keycode.GUI, 0.2, 'cmd', 0.1, Keycode.ENTER]),
        # 2nd row ----------
        (0x32ffff, 'Boot', [Keycode.GUI, 'r', -Keycode.GUI, 0.2, 'msconfig', 0.1, Keycode.ENTER]),
        (0x32ffff, 'regedit', [Keycode.GUI, 'r', -Keycode.GUI, 0.2, 'regedit', 0.1, Keycode.ENTER]),
        (0x32ffff, 'DevMan', [Keycode.GUI, 'r', -Keycode.GUI, 0.2, 'devmgmt.msc', 0.1, Keycode.ENTER]),
        # 3rd row ----------
        (0x32ffff, 'Notes', [Keycode.GUI, 'r', -Keycode.GUI, 0.2, 'notepad', 0.1, Keycode.ENTER]),
        (0x32ffff, 'Network', [Keycode.GUI, 'r', -Keycode.GUI, 0.2, 'ncpa.cpl', 0.1, Keycode.ENTER]),
        (0x32ffff, 'TskMan', [Keycode.CONTROL, Keycode.SHIFT, Keycode.ESCAPE]),
        # 4th row ----------
        (0x32ffff, 'Disks', [Keycode.GUI, 'r', -Keycode.GUI, 0.2, 'diskmgmt.msc', 0.1, Keycode.ENTER]),
        (0x32ffff, 'Resmon', [Keycode.GUI, 'r', -Keycode.GUI, 0.2, 'resmon', 0.1, Keycode.ENTER]),
        (0x32ffff, 'CPanel', [Keycode.GUI, 'r', -Keycode.GUI, 0.2, 'control', 0.1, Keycode.ENTER]),
        # Encoder button ---
        (0x000000, 'Close Window', [Keycode.ALT, Keycode.F4])
    ]
}
