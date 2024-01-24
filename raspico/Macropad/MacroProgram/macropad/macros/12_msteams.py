# SPDX-FileCopyrightText: 2021 Emma Humphries for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# MACROPAD Hotkeys: MS Teams Calls

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values
from adafruit_hid.consumer_control_code import ConsumerControlCode
DELAY_BEFORE_RETURN = 0.10
DELAY_AFTER_COMMAND = 0.80

app = {                          # REQUIRED dict, must be named 'app'
    'name' : 'Teams Video Call', # Application name
    'macros' : [                 # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x0000ff, 'Vol+', [[ConsumerControlCode.VOLUME_INCREMENT]]),
        (0x00ffff, 'Webcam', [Keycode.CONTROL, Keycode.SHIFT, 'o']),
        (0x00ff00, 'Unmute', [Keycode.CONTROL, Keycode.SPACE]),
        # 2nd row ----------
        (0x0000ff, 'Vol-', [[ConsumerControlCode.VOLUME_DECREMENT]]),
        (0x3f3f3f, '', []),
        (0xffff00, 'Hand', [Keycode.CONTROL, Keycode.SHIFT, 'k']),
        # 3rd row ----------
        (0x3f3f3f, '', []),
        (0x3f3f3f, '', []),
        (0x3f3f3f, '', []),
        # 4th row ----------
        (0xff00ff, 'Accept', [Keycode.CONTROL, Keycode.SHIFT, 'a']),
        (0x3f3f3f, '', []),
        (0xff0000, 'End', [Keycode.CONTROL, Keycode.SHIFT, 'h']),
        # Encoder button ---
        (0x000000, 'Mute', [Keycode.CONTROL, Keycode.SHIFT, 'm'])
    ]
}
