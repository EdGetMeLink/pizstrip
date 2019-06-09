import json
import logging
import time
from queue import Empty
from threading import Event, Thread

from pizstrip.excep import NoConfigError
from pizstrip.strip import get_color_class, make_strip

LOG = logging.getLogger(__name__)


class Runner(Thread):
    '''
    Main threat to updated the pixel strip in the background
    '''
    # pylint: disable=too-many-instance-attributes

    def __init__(self, queue, cfg=None, led_count=0):
        super(Runner, self).__init__()
        if not cfg:
            raise NoConfigError()

        self.exitflag = False
        self.color = get_color_class()

        self.strip = make_strip(cfg, led_count)
        self.led_count = led_count

        self.name = "Runner"
        self.queue = queue
        self.stop_event = Event()
        self.old_data = json.dumps(
            {'color': {'red': 255, 'green': 0, 'blue': 0}})
        self.nightmode = False
        nocolor = self.color(0, 0, 0)
        self.strip.begin()
        for i in range(0, self.led_count-1):
            self.strip.setPixelColor(i, nocolor)
        self.strip.show()

    def run(self):
        LOG.debug("Thread started")
        exitflag = False
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
        check the queue for new data and update strip according
        '''
        try:
            data = self.queue.get(False)
            self.queue.task_done()
            self.old_data = data
        except Empty:
            data = self.old_data
        color = self.decode(data)
        for i in range(0, self.led_count-1):
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def decode(self, data):
        '''
        decode incomming data to color
        '''
        data = json.loads(data)
        color = data['color']
        return self.color(color['red'], color['green'], color['blue'])
