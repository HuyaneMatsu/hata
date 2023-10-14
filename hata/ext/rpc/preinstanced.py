__all__ = ('DeviceType', 'ShortcutKeyType', 'VoiceConnectionState', 'VoiceSettingsModeType')

from ...discord.bases import Preinstance as P, PreinstancedBase


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
    INSTANCES : `dict` of (`str`, ``DeviceType``) items
        Stores the predefined ``DeviceType``-s. These can be accessed with their `value` as
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
        Stores the predefined ``ShortcutKeyType``-s. These can be accessed with their `value` as
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
    INSTANCES : `dict` of (`str`, ``VoiceSettingsModeType``) items
        Stores the predefined ``VoiceSettingsModeType``-s. These can be accessed with their `value` as
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


class VoiceConnectionState(PreinstancedBase):
    """
    Represents a voice connection's state.
    
    Attributes
    ----------
    name : `str`
        The name of the voice connection state.
    value : `str`
        The identifier value the voice connection state.
    
    Class Attributes
    ----------------
    INSTANCES : `dict` of (`str`, ``VoiceSettingsModeType``) items
        Stores the predefined ``VoiceSettingsModeType``-s. These can be accessed with their `value` as
        key.
    VALUE_TYPE : `type` = `str`
        The voice connection state' values' type.
    DEFAULT_NAME : `str` = `'UNDEFINED'`
        The default name of the voice connection states.
    
    Every predefined voice connection state can be accessed as class attribute as well:
    
    +-----------------------+-----------------------+---------------------------+
    | Class attribute name  | Name                  | Value                     |
    +=======================+=======================+===========================+
    | disconnected          | disconnected          | `'DISCONNECTED'`          |
    +-----------------------+-----------------------+---------------------------+
    | awaiting_endpoint      | awaiting_endpoint    | `'AWAITING_ENDPOINT'`     |
    +-----------------------+-----------------------+---------------------------+
    | authenticating        | authenticating        | `'AUTHENTICATING'`        |
    +-----------------------+-----------------------+---------------------------+
    | connecting            | connecting            | `'CONNECTING'`            |
    +-----------------------+-----------------------+---------------------------+
    | connected             | connected             | `'CONNECTED'`             |
    +-----------------------+-----------------------+---------------------------+
    | voice_disconnected    | voice_disconnected    | `'VOICE_DISCONNECTED'`    |
    +-----------------------+-----------------------+---------------------------+
    | voice_connecting      | voice_connecting      | `'VOICE_CONNECTING'`      |
    +-----------------------+-----------------------+---------------------------+
    | voice_activity        | voice_connected       | `'VOICE_CONNECTED'`       |
    +-----------------------+-----------------------+---------------------------+
    | no_route              | no_route              | `'NO_ROUTE'`              |
    +-----------------------+-----------------------+---------------------------+
    | ice_checking          | ice_checking          | `'ICE_CHECKING'`          |
    +-----------------------+-----------------------+---------------------------+
    """
    INSTANCES = {}
    VALUE_TYPE = str
    DEFAULT_NAME = 'UNDEFINED'
    
    __slots__ = ()
    
    disconnected = P('DISCONNECTED', 'disconnected')
    awaiting_endpoint = P('AWAITING_ENDPOINT', 'awaiting_endpoint')
    authenticating = P('AUTHENTICATING', 'authenticating')
    connecting = P('CONNECTING', 'connecting')
    connected = P('CONNECTED', 'connected')
    voice_disconnected = P('VOICE_DISCONNECTED', 'voice_disconnected')
    voice_connecting = P('VOICE_CONNECTING', 'voice_connecting')
    voice_connected = P('VOICE_CONNECTED', 'voice_connected')
    no_route = P('NO_ROUTE', 'no_route')
    ice_checking = P('ICE_CHECKING', 'ice_checking')
