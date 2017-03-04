#!/usr/bin/env python

import time

import scrollphathd

print("""
Scroll pHAT HD: Advanced Scrolling

Advanced scrolling example which displays a message line-by-line
and then skips back to the beginning.

Press Ctrl+C to exit.
""")

scrollphathd.rotate(180)

rewind = False
delay = 0.03

line_height = scrollphathd.DISPLAY_HEIGHT + 2

lines = ["Roses are red",
         "Violets are blue",
         "Rhyming is hard",
         "Microwave"]

lengths = [0] * len(lines)

offset_left = 0

for line, text in enumerate(lines):
    lengths[line] = scrollphathd.write_string(text, x=offset_left, y=line_height * line)
    offset_left += lengths[line]

scrollphathd.set_pixel(0, (len(lines) * line_height) - 1, 0)

current_line = 0

scrollphathd.show()

while True:
    pos_x = 0
    pos_y = 0
    for current_line in range(len(lines)):
        time.sleep(delay * 10)
        for y in range(lengths[current_line]):
            scrollphathd.scroll(1, 0)
            pos_x += 1
            time.sleep(delay)
            scrollphathd.show()
        if current_line == len(lines) - 1 and rewind:
            for y in range(pos_y):
                scrollphathd.scroll(-int(pos_x / pos_y), -1)
                scrollphathd.show()
                time.sleep(delay)
            scrollphathd.scroll_to(0, 0)
            scrollphathd.show()
            time.sleep(delay)
        else:
            for x in range(line_height):
                scrollphathd.scroll(0, 1)
                pos_y += 1
                scrollphathd.show()
                time.sleep(delay)
