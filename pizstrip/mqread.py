"""
file: mqread.py

contains mqtt functions
"""
import json
import logging
import time
from collections import namedtuple
from colorsys import hsv_to_rgb
from queue import Queue

import paho.mqtt.client as mqtt
from pizstrip.config import load_config, load_mqtt_settings
from pizstrip.excep import NoMqttConfigSection

RGB = namedtuple("RGB", ["red", "green", "blue"])

LOG = logging.getLogger("__name__")


def on_msg(mqttc, obj, msg):
    """
    callback if message received
    """
    # print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    LOG.debug("got message")
    payload = msg.payload.decode("UTF-8")
    topic = msg.topic
    LOG.debug("Message topic : %s" % topic)


def hsb_to_rgb(hsb: str) -> RGB:
    """
    convert comma separated hsb string from openhab mqtt to integer rgb value
    """
    hue, saturation, brightness = hsb.split(",")
    hue = 100 / 360 * float(hue) / 100
    rgb = hsv_to_rgb(
        round(hue, 4),
        round(float(saturation) / 100, 4),
        round(float(brightness) / 100, 4),
    )
    rgb = RGB(red=int(255 * rgb[0]), green=int(255 * rgb[1]), blue=int(255 * rgb[2]))
    LOG.debug(rgb)
    return rgb


def message_decoder(msg: str) -> RGB:
    """
    decode incomming message to RGB Color
    """
    red, green, blue = msg.split(",")
    return RGB(int(red), int(green), int(blue))


def color_topic(mqttc, obj, msg):
    """
    msg received on color topic
    """
    # TODO : error handling
    rgb = None
    msg = msg.payload.decode("UTF-8")
    if "ON" in msg:
        """
        set last known color
        """
        rgb = mqttc.last_color
    elif "OFF" in msg:
        """
        turn strip off
        """
        rgb = RGB(0, 0, 0)
    else:
        """
        decode color
        """
        rgb = message_decoder(msg)
        mqttc.last_color = rgb

    LOG.debug("mode topic received %s" % msg)
    if rgb:
        LOG.debug(json.dumps({"color": rgb._asdict()}))
        mqttc.queue.put(json.dumps({"color": rgb._asdict()}))


def setup_mqtt(cfg, queue):  # pragma: no cover # TODO: write test
    """
    setup mqtt
    """
    try:
        mqtt_conf = load_mqtt_settings(cfg)
        mqttc = mqtt.Client()
        mqttc.on_message = on_msg
        mqttc.will_set(mqtt_conf["alive_topic"], cfg.get("mqtt", "dead_message"), 1)
        mqttc.connect(mqtt_conf["server"], mqtt_conf["port"], 60)


        mqttc.message_callback_add(mqtt_conf["color_topic"], color_topic)
        mqttc.subscribe(mqtt_conf["color_topic"], 0)
        mqttc.config = mqtt_conf
        mqttc.queue = queue
        mqttc.last_color = RGB(10, 10, 10)
    except NoMqttConfigSection:
        mqttc = None
    except:
        raise
    LOG.debug("MQTT setup done")
    return mqttc


def main():  # pragma: no cover
    cfg = load_config()
    queue = Queue()
    mqttc = setup_mqtt(cfg, queue)
    mqttc.loop_start()
    exit = 0
    while exit <= 10:
        time.sleep(1)
        exit += 1
    mqttc.loop_stop()


if __name__ == "__main__":
    main()
