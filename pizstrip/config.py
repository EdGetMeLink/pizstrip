"""
file: config.py
functions to configure things or return config options
"""

from config_resolver import get_config
from pizstrip.excep import NoMqttConfigSection, NoMqttServerSetting
from typing import Dict, Any


def load_config(filename="app.ini", lookup_options=[]):
    """
    load app config
    """
    return get_config(
        app_name="pizstrip", filename=filename, lookup_options=lookup_options
    ).config


def load_mqtt_settings(cfg) -> Dict[str, Any]:
    """
    load settings for mqtt if any and return a dict with the settings or their
    defaul value
    """
    if "mqtt" in cfg.sections():
        if "server" in cfg.options("mqtt"):
            client_name = cfg.get("mqtt", "client_name")
            color_topic = cfg.get("mqtt", "color_topic")
            alive_topic = cfg.get("mqtt", "alive_topic")
            color_topic = "%s/%s" % (client_name, color_topic)
            alive_topic = "%s/%s" % (client_name, alive_topic)

            ret = {
                "server": cfg.get("mqtt", "server"),
                "port": cfg.getint("mqtt", "port", fallback=1883),
                "color_topic": color_topic,
                "alive_topic": alive_topic,
                "alive_message": cfg.get(
                    "mqtt", "alive_message", fallback="True"),
            }
        else:
            raise NoMqttServerSetting
    else:
        raise NoMqttConfigSection
    return ret
