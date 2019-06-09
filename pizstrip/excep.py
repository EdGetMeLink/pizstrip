'''
file:except.py
exceptions for piclock
'''


class NoConfigError(Exception):
    '''
    No Config Error Exception
    '''


class CharacterNotFound(Exception):
    '''
    Character not found exception
    '''


class MatrixCharError(Exception):
    '''
    Matrix Character Error
    '''


class NoMqttConfigSection(Exception):
    '''
    No MQTT config Section Error
    '''


class NoMqttServerSetting(Exception):
    '''
    No MQTT server settings in config file
    '''


class ColorClassError(Exception):
    '''
    Color Class error
    '''


class FontError(Exception):
    '''
    Font Error Class
    '''

class TemperaturReadError(Exception):
    '''
    Read Error on temperatur file
    '''
