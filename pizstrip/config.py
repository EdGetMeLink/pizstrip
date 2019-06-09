'''
file: config.py
functions to configure things or return config options
'''

from config_resolver import Config, get_config
from pizstrip.excep import NoMqttConfigSection, NoMqttServerSetting


def load_config(filename='app.ini', lookup_options=[]):
    '''
    load app config
    '''
    return get_config(
        'mds', 'pizstrip', filename=filename,
        lookup_options=lookup_options).config


def load_mqtt_settings(cfg):
    '''
    load settings for mqtt if any and return a dict with the settings or their
    defaul value
    '''
    if 'mqtt' in cfg.sections():
        if 'server' in cfg.options('mqtt'):
            ret = {
                "server": cfg.get("mqtt", "server"),
                "port": cfg.getint("mqtt", "port", fallback=1883),
                "color_topic": cfg.get(
                    "mqtt", "color_topic", fallback="pizstrip/color"),
            }
        else:
            raise NoMqttServerSetting
    else:
        raise NoMqttConfigSection
    return ret
