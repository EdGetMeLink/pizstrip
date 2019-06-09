'''
file : striprunner.py

'''
import logging
import time
from queue import Empty
from threading import Event, Thread

from pizstrip.excep import NoConfigError
from pizstrip.strip import get_color_class, make_strip

LOG = logging.getLogger(__name__)


class Striprunner(Thread):
    '''
    Runns the stripmode and sends data to the runner queue
    '''
    # pylint: disable=too-many-instance-attributes

    def __init__(self, queue, cfg=None, led_count=0):
        super(Striprunner, self).__init__()
        if not cfg:
            raise NoConfigError()

        self.exitflag = False
        self.color = get_color_class()

        self.strip = make_strip(cfg, led_count)
        self.led_count = led_count

        self.name = "Striprunner"
        self.queue = queue
        self.stop_event = Event()
        self.old_data = []
        self.nightmode = False
        nocolor = self.color(0, 0, 0)
        self.strip.begin()
        for i in range(0, self.led_count-1):
            self.strip.setPixelColor(i, nocolor)
        self.strip.show()

    def run(self):
        LOG.info("Striprunner thread started")
        while not self.exitflag:
            try:
                print("hello")
            except (KeyboardInterrupt, SystemExit):
                LOG.info("Keyboar interrupt or System Exit")
                self.exitflag = True
            except:
                LOG.exception("An error occured")
                self.exitflag = True

        LOG.info("Striprunner thread stopped")
