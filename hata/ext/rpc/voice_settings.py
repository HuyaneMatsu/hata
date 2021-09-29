__all__ = ('AvailableDevice', 'ShortcutKey', 'VoiceSettings', 'VoiceSettingsMode', 'VoiceSettingsInput',
    'VoiceSettingsOutput')

from ...discord.preconverters import preconvert_str, preconvert_preinstanced_type, preconvert_float, preconvert_int

from .preinstanced import VoiceSettingsModeType, ShortcutKeyType

class VoiceSettingsInput:
    """
    Voice input settings.
    
    Attributes
    ----------
    _available_devices_set : `bool`
        Whether `.available_devices` is set.
    available_devices : `None` or `tuple` of ``AvailableDevice``
        Voice device objects.
    device_id : `None` or `str`
        The device's identifier.
    volume : `None` or `float`
        Input voice level. Can be in range [0.0:1.0]
    """
    __slots__ = ('_available_devices_set', 'available_devices', 'device_id', 'volume')
    
    def __new__(cls, *, device_id=None, volume=None, available_devices=...):
        """
        Creates a new voice settings input object from the given parameters.
        
        Parameters
        ----------
        device_id : `str`, Optional (Keyword only)
            The device's identifier.
        volume : `float`, Optional (Keyword only)
            Input voice level. Can be in range [0.0:1.0]
        available_devices : `None` or `iterable` of ``AvailableDevice``, Optional (Keyword only)
            Voice device objects.
        
        Raises
        ------
        TypeError
            - If `device_id` is not `str` instance.
            - If `volume` is not `float` instance.
            - If `available_devices` is neither `None` nor `iterable`
            - If `available_devices` contains a non ``AvailableDevice`` instance.
        ValueError
            - If `device_id`'s length is out of range [1:2048].
            - If `volume` is out of range [0.0:1.0]
        """
        if (device_id is not None):
            device_id = preconvert_str(device_id, 'device_id', 1, 2048)
        
        if (volume is not None):
            volume = preconvert_float(volume, 'volume', 0.0, 1.0)
        
        if (available_devices is ...):
            available_devices_set = False
            available_devices_processed = None
        else:
            available_devices_set = True
            if (available_devices is None):
                available_devices_processed = None
            else:
                available_devices_processed = []
                
                available_devices_iterator = getattr(type(available_devices), '__iter__', None)
                if (available_devices_iterator is None):
                    raise TypeError(f'`available_devices` can be `None` or an `iterable`, got '
                        f'{available_devices.__class__.__name__}.')
                
                for available_device in available_devices_iterator(available_devices):
                    if not isinstance(available_device, AvailableDevice):
                        raise TypeError(f'`available_devices` can contain {AvailableDevice.__name__} instances, got '
                            f'{available_device.__class__.__name__}.')
                    
                    available_devices_processed.append(available_device)
                
                if available_devices_processed:
                    available_devices_processed = tuple(available_devices_processed)
                else:
                    available_devices_processed = None
        
        self = object.__new__(cls)
        self.device_id = device_id
        self.volume = volume
        self.available_devices = available_devices_processed
        self._available_devices_set = available_devices_set
        
        return self
    
    
    def __repr__(self):
        """Returns the voice settings input's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        
        device_id = self.device_id
        if (device_id is None):
            field_added = False
        else:
            field_added = True
            
            repr_parts.append(' device_id=')
            repr_parts.append(repr(device_id))
        
        
        volume = self.volume
        if (volume is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' volume=')
            repr_parts.append(repr(self.volume))
        
        
        if self._available_devices_set:
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append('available_devices=')
            
            available_devices = self.available_devices
            if (available_devices is None):
                repr_parts.append('[]')
            else:
                repr_parts.append('[')
                
                index = 0
                limit = len(repr_parts)
                
                while True:
                    available_device = available_devices[index]
                    index += 1
                    
                    repr_parts.append(repr(available_device))
                    
                    if index == limit:
                        break
                    
                    repr_parts.append(', ')
                    continue
                
                repr_parts.append(']')
        
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def to_data(self):
        """
        Converts the voice settings input to json serializible object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {}
        
        device_id = self.device_id
        if (device_id is not None):
            data['device_id'] = self.device_id
        
        volume = self.volume
        if (volume is not None):
            data['volume'] = volume
        
        if self._available_devices_set:
            available_devices = self.available_devices
            if available_devices is None:
                available_devices = ()
            
            data['available_devices'] = available_devices
        
        return data
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new voice settings input object from the given json data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Voice settings input data.
        
        Returns
        -------
        self : ``VoiceSettingsInput``
        """
        self = object.__new__(cls)
        self._available_devices_set = True
        
        self.device_id = data['device_id']
        self.volume = data['volume']*0.01
        
        available_devices_data = data.get('available_devices', None)
        if (available_devices_data is None) or (not available_devices_data):
            available_devices = None
        else:
            available_devices = tuple(
                AvailableDevice.from_data(available_device_data) for available_device_data in available_devices_data
            )
        self.available_devices = available_devices
        
        return self
        

class AvailableDevice:
    """
    Available voice input or output device.
    
    Attributes
    ----------
    id : `str`
        Identifier of the device.
    name : `str`
        The device's name.
    """
    __slots__ = ('id', 'name')
    
    def __new__(cls, id_, name):
        """
        Creates a new available device instance.
        
        Parameters
        ----------
        id_ : `str`
            The identifier of the device.
        name : `str`
            The device's name.
        
        Raises
        ------
        TypeError
            - If `id_` is not `str` instance.
            - If `name` is not `str` instance`.
        ValueError
            - If `id_`'s length is out of range [1:2048].
            - If `name`'s length is out of range [1:2048].
        """
        id_ = preconvert_str(id_, 'id_', 1, 2048)
        name = preconvert_str(name, 'name', 1, 2048)
        
        self = object.__new__(cls)
        self.id = id_
        self.name = name
        return self
    
    
    def __repr__(self):
        """Returns the device's representation."""
        return f'<{self.__class__.__name__} id={self.id!r}, name={self.name!r}>'
    
    
    def to_data(self):
        """
        Converts the available device to json serializible object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        return {
            'id_': self.id_,
            'name': self.name,
        }
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new available device object from the given json data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Available device data.
        
        Returns
        -------
        self : ``AvailableDevice``
        """
        self = object.__new__(cls)
        self.id = data['id']
        self.name = data['name']
        return self


class VoiceSettingsOutput:
    """
    Voice output settings.
    
    Attributes
    ----------
    _available_devices_set : `bool`
        Whether `.available_devices` is set.
    available_devices : `None` or `tuple` of ``AvailableDevice``
        Voice device objects.
    device_id : `None` or `str`
        The device's identifier.
    volume : `None` or `float`
        Output voice level. Can be in range [0.0:2.0]
    """
    __slots__ = ('_available_devices_set', 'available_devices', 'device_id', 'volume')
    
    def __new__(cls, *, device_id=None, volume=None, available_devices=...):
        """
        Creates a new voice settings output object from the given parameters.
        
        Parameters
        ----------
        device_id : `str`, Optional (Keyword only)
            The device's identifier.
        volume : `float`, Optional (Keyword only)
            Output voice level. Can be in range [0.0:2.0]
        available_devices : `None` or `iterable` of ``AvailableDevice``, Optional (Keyword only)
            Voice device objects.
        
        Raises
        ------
        TypeError
            - If `device_id` is not `str` instance.
            - If `volume` is not `float` instance.
            - If `available_devices` is neither `None` nor `iterable`
            - If `available_devices` contains a non ``AvailableDevice`` instance.
        ValueError
            - If `device_id`'s length is out of range [1:2048].
            - If `volume` is out of range [0.0:2.0]
        """
        if (device_id is not None):
            device_id = preconvert_str(device_id, 'device_id', 1, 2048)
        
        if (volume is not None):
            volume = preconvert_float(volume, 'volume', 0.0, 2.0)
        
        if (available_devices is ...):
            available_devices_set = False
            available_devices_processed = None
        else:
            available_devices_set = True
            if (available_devices is None):
                available_devices_processed = None
            else:
                available_devices_processed = []
                
                available_devices_iterator = getattr(type(available_devices), '__iter__', None)
                if (available_devices_iterator is None):
                    raise TypeError(f'`available_devices` can be `None` or an `iterable`, got '
                        f'{available_devices.__class__.__name__}.')
                
                for available_device in available_devices_iterator(available_devices):
                    if not isinstance(available_device, AvailableDevice):
                        raise TypeError(f'`available_devices` can contain {AvailableDevice.__name__} instances, got '
                            f'{available_device.__class__.__name__}.')
                    
                    available_devices_processed.append(available_device)
                
                if available_devices_processed:
                    available_devices_processed = tuple(available_devices_processed)
                else:
                    available_devices_processed = None
        
        self = object.__new__(cls)
        self.device_id = device_id
        self.volume = volume
        self.available_devices = available_devices_processed
        self._available_devices_set = available_devices_set
        
        return self
    
    
    def __repr__(self):
        """Returns the voice settings output's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        
        device_id = self.device_id
        if (device_id is None):
            field_added = False
        else:
            field_added = True
            
            repr_parts.append(' device_id=')
            repr_parts.append(repr(device_id))
        
        
        volume = self.volume
        if (volume is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' volume=')
            repr_parts.append(repr(self.volume))
        
        
        if self._available_devices_set:
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append('available_devices=')
            
            available_devices = self.available_devices
            if (available_devices is None):
                repr_parts.append('[]')
            else:
                repr_parts.append('[')
                
                index = 0
                limit = len(repr_parts)
                
                while True:
                    available_device = available_devices[index]
                    index += 1
                    
                    repr_parts.append(repr(available_device))
                    
                    if index == limit:
                        break
                    
                    repr_parts.append(', ')
                    continue
                
                repr_parts.append(']')
        
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def to_data(self):
        """
        Converts the voice settings output to json serializible object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {}
        
        device_id = self.device_id
        if (device_id is not None):
            data['device_id'] = self.device_id
        
        volume = self.volume
        if (volume is not None):
            data['volume'] = volume
        
        if self._available_devices_set:
            available_devices = self.available_devices
            if available_devices is None:
                available_devices = ()
            
            data['available_devices'] = available_devices
        
        return data
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new voice settings output object from the given json data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Voice settings output data.
        
        Returns
        -------
        self : ``VoiceSettingsOutput``
        """
        self = object.__new__(cls)
        self._available_devices_set = True
        
        self.device_id = data['device_id']
        self.volume = data['volume']*0.01
        
        available_devices_data = data.get('available_devices', None)
        if (available_devices_data is None) or (not available_devices_data):
            available_devices = None
        else:
            available_devices = tuple(
                AvailableDevice.from_data(available_device_data) for available_device_data in available_devices_data
            )
        self.available_devices = available_devices
        
        return self


class VoiceSettingsMode:
    """
    Voice setting mode.
    
    Attributes
    ----------
    _shortcut_combination_set : `bool`
        Whether the shortcut attribute is set.
    auto_threshold : `None` or `bool`
        Whether the voice activity should automatically set it's threshold.
    delay : `None` or `float`
        The push to talk release delay in seconds. Can be in range [0.0:2.0].
    shortcut_combination : `None` or `tuple` of ``ShortcutKey``
        Shortcut key combo for push to talk.
    threshold : `None` or `float`
        Threshold  for voice activity in dB. Can be in range [-100.0:0.0].
    type : `None` or ``VoiceSettingsModeType``
        Voice setting mode type.
    """
    __slots__ = ('_shortcut_combination_set', 'auto_threshold', 'delay', 'shortcut_combination', 'threshold', 'type')
    
    def __new__(cls, *, type_=None, auto_threshold=None, threshold=None, shortcut_combination=..., delay=None):
        """
        Creates a new voice setting mode instance from the given parameters.
        
        Parameters
        ----------
        type_ : ``VoiceSettingsModeType`` or `str`, Optional (Keyword only)
            Voice setting mode type.
        auto_threshold : `bool`, Optional (Keyword only)
            Whether the voice activity should automatically set it's threshold.
        threshold : `float`, Optional (Keyword only)
            Threshold  for voice activity in dB. Can be in range [-100.0:0.0]
        shortcut_combination : `None`, ``ShortcutKey``, Optional (Keyword only)
            Shortcut key combo for push to talk.
        delay : `float`, Optional (Keyword only)
            The push to talk release delay in seconds. Can be in range [0.0:2.0]
        
        Raises
        ------
        TypeError
            - If `type` is neither `str`, nor ``VoiceSettingsModeType`` instance.
            - If `threshold` is not `float` instance.
            - If `shortcut_combination` is not `None`, ``ShortcutKey`` nor `iterable` of ``ShortcutKey``.
            - If `delay` is not `float` instance.
        ValueError
            - If `threshold` is out of range [-100.0:0]
            - If `delay` is out of range [0.0:2.0]
        AssertionError
            If `auto_threshold` is not `bool` instance.
        """
        if (type_ is not None):
            type_ = preconvert_preinstanced_type(type_, 'type_', VoiceSettingsModeType)
        
        if __debug__:
            if (auto_threshold is not None) and (not isinstance(auto_threshold, bool)):
                raise AssertionError(f'`auto_threshold` can be given as `bool` instance, got '
                    f'{auto_threshold.__class__.__name__}')
        
        if (threshold is not None):
            threshold = preconvert_float(threshold, 'threshold', -100.0, 0.0)
        
        if (shortcut_combination is ...):
            shortcut_combination_processed = None
            shortcut_combination_set = False
        else:
            shortcut_combination_set = True
            if shortcut_combination is None:
                shortcut_combination_processed = None
            elif isinstance(shortcut_combination, ShortcutKey):
                shortcut_combination_processed = (shortcut_combination, )
            else:
                shortcut_combination_iterator = getattr(type(shortcut_combination), '__iter__', None)
                if (shortcut_combination_iterator is None):
                    raise TypeError(f'`shortcut_combination` can be given as `None`, `{ShortcutKey.__name__}` '
                        f'instance, or as an `iterable` of `{ShortcutKey.__name__}` instances, got '
                        f'{shortcut_combination.__class__.__name__}.')
                
                shortcut_combination_processed = []
                for shortcut in shortcut_combination_iterator(shortcut_combination):
                    if not isinstance(shortcut, ShortcutKey):
                        raise TypeError(f'`shortcut_combination` contains non `{ShortcutKey.__name__}` instance, got '
                            f'{shortcut.__class__.__name__}.')
                    
                    shortcut_combination_processed.append(shortcut)
                
                if shortcut_combination_processed:
                    shortcut_combination_processed = tuple(shortcut_combination_processed)
                else:
                    shortcut_combination_processed = None
            
        if (delay is not None):
            delay = preconvert_float(delay, 'delay', 0.0, 2.0)
        
        self = object.__new__(cls)
        self._shortcut_combination_set = shortcut_combination_set
        self.type = type_
        self.auto_threshold = auto_threshold
        self.threshold = threshold
        self.shortcut_combination = shortcut_combination_processed
        self.delay = delay
        return self
    
    
    def __repr__(self):
        """Returns the voice setting mode's representation."""
        repr_parts = ['<', self.__class__.__name__,]
        
        
        type_ = self.type
        if (type_ is None):
            field_added = False
        else:
            field_added = True
            
            repr_parts.append(' type=')
            repr_parts.append(type_.name)
            repr_parts.append(' (')
            repr_parts.append(repr(type_.value))
            repr_parts.append(')')
        
        
        auto_threshold = self.auto_threshold
        if (auto_threshold is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' auto_threshold=')
            repr_parts.append(repr(auto_threshold))
        
        
        threshold = self.threshold
        if (threshold is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' threshold=')
            repr_parts.append(repr(threshold))
        
        
        delay = self.delay
        if (delay is not None):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' delay=')
            repr_parts.append(repr(delay))
        
        
        if self._shortcut_combination_set:
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' shortcut_combination=')
            
            shortcut_combination = self.shortcut_combination
            if (shortcut_combination is None):
                repr_parts.append('[]')
            else:
                repr_parts.append('[')
                
                index = 0
                limit = len(shortcut_combination)
                
                while True:
                    shortcut = shortcut_combination[index]
                    index += 1
                    
                    repr_parts.append(repr(shortcut))
                    if index == limit:
                        break
                    
                    repr_parts.append(', ')
                    continue
                
                repr_parts.append(']')
        
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def to_data(self):
        """
        Converts the voice settings mode to json serializible object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {}
        
        auto_threshold = self.auto_threshold
        if (auto_threshold is not None):
            data['auto_threshold'] = auto_threshold
        
        delay = self.delay
        if (delay is not None):
            data['delay'] = delay*1000.0
        
        if self._shortcut_combination_set:
            shortcut_combination = self.shortcut_combination
            if shortcut_combination is None:
                shortcut_combination_data = []
            else:
                shortcut_combination_data = [shortcut.to_data() for shortcut in shortcut_combination]
            
            data['shortcut'] = shortcut_combination_data
        
        threshold = self.threshold
        if (threshold is not None):
            data['threshold'] = threshold
        
        type_ = self.type
        if (type_ is not None):
            data['type'] = type_.value
        
        return data
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new voice settings mode object from the given json data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Voice settings mode data.
        
        Returns
        -------
        self : ``VoiceSettingsMode``
        """
        shortcut_combination_data = data.get('shortcut', None)
        if (shortcut_combination_data is None) or (not shortcut_combination_data):
            shortcut_combination = None
        else:
            shortcut_combination = tuple(
                ShortcutKey.from_data(shortcut_data) for shortcut_data in shortcut_combination_data
            )
        
        self = object.__new__(cls)
        self.auto_threshold = data['auto_threshold']
        self.delay = data['delay']*0.001
        self.shortcut_combination = shortcut_combination
        self.threshold = data['threshold']
        self.type = VoiceSettingsModeType.get(data['type'])
        return self


class ShortcutKey:
    """
    Shortcut key for push to talk.
    
    Attributes
    ----------
    code : `int`
        The key's code.
    name : `str`
        The key's name.
    type : ``ShortcutKeyType``
        The key's type.
    """
    __slots__ = ('code', 'name', 'type')
    
    def __new__(cls, type_, code, name):
        """
        Creates a new shortcut key instance from the given parameters.
        
        Parameters
        ----------
        type_ : ``ShortcutKeyType`` or `int`
            The key's type.
        code : `int`
            The key's code.
        name : `str`
            The key's name.
        
        Raises
        ------
        TypeError
            - If `type_` is neither ``ShortcutKeyType`` nor `int` instance.
            - If `code` is not `int` instance.
            - If `name` is not `str` instance.
        ValueError
            - If `code` is out of int64 range.
            - If `name`'s length is out of range [1:2048].
        """
        type_ = preconvert_preinstanced_type(type_, 'type_', ShortcutKey)
        code = preconvert_int(code, 'code', -(1<<63), (1<<63)-1)
        name = preconvert_str(name, 'name', 1, 2048)
        
        self = object.__new__(cls)
        self.type = type_
        self.code = code
        self.name = name
        return self
    
    
    def __repr__(self):
        """Returns the shortcut key's representation."""
        repr_parts = ['<', self.__class__.__name__, ' type=']
        
        type_ = self.type
        repr_parts.append(type_.name)
        repr_parts.append(' (')
        repr_parts.append(repr(type_.value))
        repr_parts.append(
            ')'
            ', code'
        )
        
        repr_parts.append(repr(self.code))
        
        repr_parts.append(', name=')
        repr_parts.append(repr(self.name))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def to_data(self):
        """
        Converts the shortcut key to json serializible object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        return {
            'type': self.type.value,
            'code': self.code,
            'name': self.name,
        }
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new shortcut key object from the given json data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Shortcut key data.
        
        Returns
        -------
        self : ``ShortcutKey``
        """
        self = object.__new__(cls)
        self.type = ShortcutKeyType.get(data['type'])
        self.code = data['code']
        self.name = data['name']
        return self


class VoiceSettings:
    """
    Represents a user's voice settings.
    
    Attributes
    ----------
    automatic_gain_control : `bool`
        Whether automatic gain control is enabled.
    deaf : `bool`
        Whether the user is deaf.
    echo_cancellation : `bool`
        Whether echo cancellation is enabled.
    input : ``VoiceSettingsInput``
        Input settings.
    mode : ``VoiceSettingsMode``
        Voice mode settings.
    mute : `bool`
        Whether the user is muted.
    noise_suppression : `bool`
        Whether noise suppression is enabled.
    output : ``VoiceSettingsOutput``
        Output settings.
    quality_of_service : `bool`
        Whether voice quality of service is enabled.
        
        > QoS, quality of service is a method to prioritize network traffic going through a router to provide
        > acceptable service to most users.
    silence_warning : `bool`
        Whether silence warning notice is enabled.
    """
    __slots__ = ('automatic_gain_control', 'deaf', 'echo_cancellation', 'input', 'mode', 'mute', 'noise_suppression',
        'output', 'quality_of_service', 'silence_warning')
    
    def __repr__(self):
        """Returns the voice setting's representation"""
        repr_parts = ['<', self.__class__.__name__]
        
        
        repr_parts.append(' automatic_gain_control=')
        repr_parts.append(repr(self.automatic_gain_control))
        
        
        repr_parts.append(', deaf=')
        repr_parts.append(repr(self.deaf))
        
        
        repr_parts.append(', echo_cancellation=')
        repr_parts.append(repr(self.echo_cancellation))
        
        
        repr_parts.append(', input=')
        repr_parts.append(repr(self.input))
        
        
        repr_parts.append(', mode=')
        repr_parts.append(repr(self.mode))
        
        
        repr_parts.append(', mute=')
        repr_parts.append(repr(self.mute))
        
        
        repr_parts.append(', noise_suppression=')
        repr_parts.append(repr(self.noise_suppression))
        
        
        repr_parts.append(', output=')
        repr_parts.append(repr(self.output))
        
        
        repr_parts.append(', quality_of_service=')
        repr_parts.append(repr(self.quality_of_service))
        
        
        repr_parts.append(', silence_warning=')
        repr_parts.append(repr(self.silence_warning))
        
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new voice settings object from the given json data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Voice settings data.
        
        Returns
        -------
        self : ``VoiceSettings``
        """
        self = object.__new__(cls)
        self.automatic_gain_control = data['automatic_gain_control']
        self.deaf = data['deaf']
        self.echo_cancellation = data['echo_cancellation']
        self.input = VoiceSettingsInput.from_data(data['input'])
        self.mode = VoiceSettingsMode.from_data(data['mode'])
        self.mute = data.get('mute', False)
        self.noise_suppression = data['noise_suppression']
        self.output = VoiceSettingsOutput.from_data(data['output'])
        self.quality_of_service = data['qos']
        self.silence_warning = data['silence_warning']
        return self
