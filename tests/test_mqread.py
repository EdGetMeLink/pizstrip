'''
file: test_mqread.py

contains tests for message queue read tests
'''
from collections import namedtuple
from queue import Queue
from unittest.mock import patch

from pizstrip.mqread import hsb_to_rgb, mode_topic, on_msg, params_topic

MQTTC = namedtuple("MQTTC", ["config", "queue"])
MSG = namedtuple("MSG", ["topic", "payload", "qos"])
RGB = namedtuple("RGB", ['red', 'green', 'blue'])


def test_onmessage_unknown_topic():
    '''
    test on message function if topic is unknown
    '''
    config = {"mode_topic": "mode", "color_topic": "color"}
    queue = []
    mqttc = MQTTC(config=config, queue=queue)
    msg = MSG(topic="foo".encode('UTF-8'),
              payload='123,123,123'.encode('UTF-8'), qos=2)
    with patch('pizstrip.mqread.mode_topic') as mom:
        on_msg(mqttc, "a", msg)
        mom.assert_not_called()
    with patch('pizstrip.mqread.params_topic') as mom:
        on_msg(mqttc, "a", msg)
        mom.assert_not_called()


def test_mode_topic():
    '''
    test mqtt mode topic function
    '''
    config = {"mode_topic": "mode", "params_topic": "params"}
    queue = Queue()
    mqttc = MQTTC(config=config, queue=queue)
    msg = MSG(topic="mode",
              payload='unicolor'.encode('UTF-8'), qos=2)
    mode_topic(mqttc, 1, msg)
    result = queue.get()
    expected = {'mode': 'unicolor'}
    assert result == expected


def test_params_topic():
    '''
    test mqtt params topic function
    '''
    config = {"mode_topic": "mode", "params_topic": "params"}
    queue = Queue()
    mqttc = MQTTC(config=config, queue=queue)
    msg = MSG(topic="params",
              payload='blah'.encode('UTF-8'), qos=2)
    params_topic(mqttc, 1, msg)
    result = queue.get()
    expected = {'params': 'blah'}
    assert result == expected


def test_hsb2rgb():
    '''
    test funtion hsb_to_rgb
    '''
    rgb = hsb_to_rgb('10,10,10')
    expected = RGB(25, 23, 22)
    assert rgb == expected
