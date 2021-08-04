__all__ = ('DeviceType', 'ShortcutKeyType', 'VoiceSettingsModeType')

from ...discord.bases import PreinstancedBase, Preinstance as P


class DeviceType(PreinstancedBase):
    """
    Represents a device's type.
    
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
    VALUE_TYPE : `type` = `str`
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
    
    audio_input = P('audioinput', 'audio_input')
    audio_output = P('audiooutput', 'audio_output')
    video_input = P('videoinput', 'video_input')


class ShortcutKeyType(PreinstancedBase):
    """
    Represents an key' type.
    
    Attributes
    ----------
    name : `str`
        The name of the key type.
    value : `str`
        The identifier value the key type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``ShortcutKeyType``) items
        Stores the predefined ``ShortcutKeyType`` instances. These can be accessed with their `value` as
        key.
    VALUE_TYPE : `type` = `int`
        The key types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the key types.
    
    Every predefined key type can be accessed as class attribute as well:
    
    +-----------------------+-----------------------+-------+
    | Class attribute name  | Name                  | Value |
    +=======================+=======================+=======+
    | keyboard_key          | keyboard_key          | `0`   |
    +-----------------------+-----------------------+-------+
    | mouse_button          | mouse_button          | `1`   |
    +-----------------------+-----------------------+-------+
    | keyboard_modified_key | keyboard_modified_key | `2`   |
    +-----------------------+-----------------------+-------+
    | gamepad_button        | gamepad_button        | `3`   |
    +-----------------------+-----------------------+-------+
    """
    INSTANCES = {}
    VALUE_TYPE = int
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    keyboard_key = P(0, 'keyboard_key')
    mouse_button = P(1, 'mouse_button')
    keyboard_modified_key = P(2, 'keyboard_modified_key')
    gamepad_button = P(3, 'gamepad_button')



class VoiceSettingsModeType(PreinstancedBase):
    """
    Represents a voice setting mode's type.
    
    Attributes
    ----------
    name : `str`
        The name of the voice setting mode type.
    value : `str`
        The identifier value the voice setting mode type.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`int`, ``VoiceSettingsModeType``) items
        Stores the predefined ``VoiceSettingsModeType`` instances. These can be accessed with their `value` as
        key.
    VALUE_TYPE : `type` = `str`
        The voice setting mode types' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the voice setting mode types.
    
    Every predefined voice setting mode type can be accessed as class attribute as well:
    
    +-----------------------+-------------------+-----------------------+
    | Class attribute name  | Name              | Value                 |
    +=======================+===================+=======================+
    | push_to_talk          | push_to_talk      | `'PUSH_TO_TALK'`      |
    +-----------------------+-------------------+-----------------------+
    | voice_activity        | voice_activity    | `'VOICE_ACTIVITY'`    |
    +-----------------------+-------------------+-----------------------+
    """
    INSTANCES = {}
    VALUE_TYPE = str
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    audio_input = P('PUSH_TO_TALK', 'audio_input')
    audio_output = P('VOICE_ACTIVITY', 'audio_output')
