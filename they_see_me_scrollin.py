import time

import scrollphathd
from scrollphathd.fonts import font5x7

scrollphathd.rotate(180)


def display_string(string):
    print('[Display] Showing message "{0}"'.format(string))
    string += '      '
    buffer = scrollphathd.write_string(string, x=17, y=0, font=font5x7, brightness=0.5)

    for i in range(buffer):
        scrollphathd.show()
        scrollphathd.scroll(1)
        time.sleep(0.02)

    scrollphathd.scroll_to(0, 0)
    scrollphathd.clear()
    scrollphathd.show()
