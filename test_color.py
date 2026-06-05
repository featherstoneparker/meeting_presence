#!/usr/bin/env python
"""Quick tool to test colors on the Blynclight. Usage: python test_color.py FF0000"""
import sys
from blynclight import BlyncLight

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip("#")
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

if len(sys.argv) != 2:
    print("Usage: python test_color.py <hex>  e.g. FFB300")
    sys.exit(1)

r, g, b = hex_to_rgb(sys.argv[1])
light = BlyncLight.get_light()
with light.updates_paused():
    light.red = r
    light.green = g
    light.blue = b
    light.on = 1

print(f"Set to #{sys.argv[1].upper()} ({r}, {g}, {b})")
