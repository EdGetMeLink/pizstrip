'''
file: stripmodes.py
contains different modes for the led strip
'''

import logging
import time
from datetime import datetime
from queue import Empty
from threading import Event, Thread

from pizstrip.excep import NoConfigError
from pizstrip.strip import get_color_class, make_strip

LOG = logging.getLogger(__name__)


class Stripmode(Thread):
    '''
    Master Stripmode class
    '''

    def __init__(self, queue, strip, led_count=None):
        super(Stripmode, self).__init__()

        self.exitflag = False
        self.color = get_color_class()
        self.strip = strip
        self.led_count = led_count

        self.name = "Stripmode initial"
        self.stripmode = self.stripmode0
        self.queue = queue
        self.stop_event = Event()
        self.old_data = []
        nocolor = self.color(0, 0, 0)
        self.strip.begin()
        for i in range(0, self.led_count-1):
            self.strip.setPixelColor(i, nocolor)
        self.strip.show()

    def run(self):
        LOG.info("Thread started")
        self.exitflag = False
        while not self.exitflag:
            try:
                self.update_strip()
                time.sleep(0.1)
            except (KeyboardInterrupt, SystemExit):
                LOG.info("Keyboar interrupt or System Exit")
                self.exitflag = True
            except:
                LOG.exception("An error occured")
                self.exitflag = True

        LOG.info("thread stopped")


    def update_strip(self):
        '''
        '''
        for idx, color in enumerate(self.stripmode()):
            self.strip.setPixelColor(idx, color)
        self.strip.show()

    def stripmode0(self, params=None):
        '''
        Stripmode 0 if no params given default is used
        '''
        for pixel in range(0, self.led_count - 1):
            yield(self.color(100, 100, 100))
