'''
file : main.py
contains the entriepoint for pizstrip
'''
import logging
import logging.handlers
import time
from datetime import datetime
from queue import Empty, Queue
from threading import Event

from pizstrip.config import load_config
from pizstrip.excep import ColorClassError, TemperaturReadError
from pizstrip.helpers import clear_screen
from pizstrip.mqread import RGB, setup_mqtt
from pizstrip.runner import Runner
from pizstrip.strip import Color, get_color_class

LOG = logging.getLogger(__name__)


def setup_logging():  # pragma:no cover
    '''
    setup logging
    '''
    log_file = "pizstrip.log"
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    formatter = ColorFormatter(
        '%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s')

    file_handler = logging.handlers.RotatingFileHandler(log_file,
                                                        maxBytes=1024*1024,
                                                        backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


class ColorFormatter(logging.Formatter):
    pass


def check_mqqueue(queue):
    try:
        data = queue.get(False)
        queue.task_done()
        LOG.debug("got data on color queue : %s" % data)
    except Empty:
        data = None
    return data


def start_runner(queue, cfg):
    runner = Runner(queue, cfg, led_count=256)
    runner.daemon = True
    runner.start()
    return runner


def convert_to_color(rgb, color: Color):
    '''
    convert from RGB to Color
    '''
    return color(rgb.red, rgb.green, rgb.blue)


def get_strip(queue, old_mode, old_params):
    '''
    check mqqueue and return strip
    '''
    data = check_mqqueue(queue)
    if data:
        mode = data.get('mode', old_mode)
        params = data.get('params', old_params)
    else:
        mode = old_mode
        params = old_params
    color = get_color_class()

    strip = ''
    return strip



def start():
    cfg = load_config()
    clear_screen()
    setup_logging()
    queue = Queue()
    runner = start_runner(queue, cfg)
    mqttc = setup_mqtt(cfg, queue)
    mqttc.loop_start()

    color = get_color_class()

    while runner.isAlive():
        try:
            pass
        except (KeyboardInterrupt, SystemExit):
            LOG.info("Stopped by Keyboard or System Exit")
            runner.exitflag = True
            runner.join()
            mqttc.loop_stop()
        except Exception:
            LOG.exception("Exception caused crash")
            runner.exitflag = True
            runner.join()
            mqttc.loop_stop()
            raise


if __name__ == "__main__":
    start()
