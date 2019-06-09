'''
file: test_config.py

contains test for the pizstrip config
'''

from pizstrip.config import load_config, load_mqtt_settings
from pizstrip.excep import NoMqttConfigSection, NoMqttServerSetting


def test_load_mqtt_settings():
    '''
    load mqtt settings from config file
    '''
    cfg = load_config(
        filename='app.test.ini',
        lookup_options={'search_path': 'tests/testdata'})
    mqtt = load_mqtt_settings(cfg)
    expected = {
        "server": "test.server.local",
        "port": 1883,
        "fg_topic": "pizstrip/fg",
        "bg_topic": "pizstrip/bg",
    }

    assert mqtt == expected


def test_load_missing_mqtt_settings():
    '''
    load mqtt settings from config file
    '''
    cfg = load_config(
        filename='app.test.nomqtt.ini',
        lookup_options={'search_path': 'tests/testdata'})
    try:
        load_mqtt_settings(cfg)
        result = False
    except NoMqttConfigSection:
        result = True
    assert result


def test_load_mqtt_default_settings():
    '''
    load mqtt settings from config file
    '''
    cfg = load_config(
        filename='app.test.default_mqtt.ini',
        lookup_options={'search_path': 'tests/testdata'})
    mqtt = load_mqtt_settings(cfg)
    expected = {
        "server": "test.server.local",
        "port": 1883,
        "fg_topic": "pizstrip/fg",
        "bg_topic": "pizstrip/bg",
    }

    assert mqtt == expected


def test_load_mqtt_no_server_settings():
    '''
    load mqtt settings from config file
    '''
    cfg = load_config(
        filename='app.test.no_mqtt_server.ini',
        lookup_options={'search_path': 'tests/testdata'})
    try:
        load_mqtt_settings(cfg)
        ret = False
    except NoMqttServerSetting:
        ret = True
    assert ret
