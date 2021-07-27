__all__ = ('DeviceType', )

from ...discord.bases import PreinstancedBase, Preinstance as P


class DeviceType(PreinstancedBase):
    """
    Represents an device' type.
    
    Attributes
    ----------
    name : `str`
        The name of the device type.
    value : `str`
        The identifier value the device type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``DeviceType``) items
        Stores the predefined ``DeviceType`` instances. These can be accessed with their `value` as
        key.
    VALUE_TYPE : `type` = `int`
        The device types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the device types.
    
    Every predefined device type can be accessed as class attribute as well:
    
    +-----------------------+-------------------+-------------------+
    | Class attribute name  | Name              | Value             |
    +=======================+===================+===================+
    | audio_input           | audio_input       | `'audioinput'`    |
    +-----------------------+-------------------+-------------------+
    | audio_output          | audio_output      | `'audiooutput'`   |
    +-----------------------+-------------------+-------------------+
    | video_input           | video_input       | `'videoinput'`    |
    +-----------------------+-------------------+-------------------+
    """
    INSTANCES = {}
    VALUE_TYPE = str
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    audio_input = P('audioinput', 'audio_input',)
    audio_output = P('audiooutput', 'audio_output',)
    video_input = P('videoinput', 'video_input',)
