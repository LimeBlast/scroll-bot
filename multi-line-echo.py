#!/usr/bin/env python
import time

import scrollphathd
from scrollphathd.fonts import font5x7

scrollphathd.rotate(180)

lines = ["In the old #BILGETANK we'll keep you in the know",
         "In the old #BILGETANK we'll fix your techie woes",
         "And we'll make things",
         "And we'll break things",
         "'til we're altogether aching",
         "Then we'll grab a cup of grog down in the old #BILGETANK"]

for line, text in enumerate(lines):
    text += '      '
    buffer = scrollphathd.write_string(text, x=17, y=0, font=font5x7, brightness=0.5)

    for i in range(buffer):
        scrollphathd.show()
        scrollphathd.scroll(1)
        time.sleep(0.02)

    scrollphathd.scroll_to(0, 0)
    scrollphathd.show()
