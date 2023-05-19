__all__ = (
    'ChannelMix', 'Distortion', 'Equalizer', 'Filter', 'Karaoke', 'LowPass', 'Rotation', 'Timescale', 'Tremolo',
    'Vibrato', 'Volume'
)

from scarletio import RichAttributeErrorBaseType, copy_docs

from .constants import (
    LAVALINK_BAND_COUNT, LAVALINK_KEY_FILTER_CHANNEL_MIX, LAVALINK_KEY_FILTER_CHANNEL_MIX_LEFT_TO_LEFT,
    LAVALINK_KEY_FILTER_CHANNEL_MIX_LEFT_TO_RIGHT, LAVALINK_KEY_FILTER_CHANNEL_MIX_RIGHT_TO_LEFT,
    LAVALINK_KEY_FILTER_CHANNEL_MIX_RIGHT_TO_RIGHT, LAVALINK_KEY_FILTER_DISTORTION,
    LAVALINK_KEY_FILTER_DISTORTION_COS_OFFSET, LAVALINK_KEY_FILTER_DISTORTION_COS_SCALE,
    LAVALINK_KEY_FILTER_DISTORTION_OFFSET, LAVALINK_KEY_FILTER_DISTORTION_SCALE,
    LAVALINK_KEY_FILTER_DISTORTION_SIN_OFFSET, LAVALINK_KEY_FILTER_DISTORTION_SIN_SCALE,
    LAVALINK_KEY_FILTER_DISTORTION_TAN_OFFSET, LAVALINK_KEY_FILTER_DISTORTION_TAN_SCALE, LAVALINK_KEY_FILTER_EQUALIZER,
    LAVALINK_KEY_FILTER_EQUALIZER_BAND, LAVALINK_KEY_FILTER_EQUALIZER_GAIN, LAVALINK_KEY_FILTER_KARAOKE,
    LAVALINK_KEY_FILTER_KARAOKE_FILTER_BAND, LAVALINK_KEY_FILTER_KARAOKE_FILTER_WIDTH,
    LAVALINK_KEY_FILTER_KARAOKE_LEVEL, LAVALINK_KEY_FILTER_KARAOKE_MONO_LEVEL, LAVALINK_KEY_FILTER_LOW_PASS,
    LAVALINK_KEY_FILTER_LOW_PASS_SMOOTHING, LAVALINK_KEY_FILTER_ROTATION, LAVALINK_KEY_FILTER_ROTATION_ROTATION,
    LAVALINK_KEY_FILTER_TIMESCALE, LAVALINK_KEY_FILTER_TIMESCALE_PITCH, LAVALINK_KEY_FILTER_TIMESCALE_RATE,
    LAVALINK_KEY_FILTER_TIMESCALE_SPEED, LAVALINK_KEY_FILTER_TREMOLO, LAVALINK_KEY_FILTER_TREMOLO_DEPTH,
    LAVALINK_KEY_FILTER_TREMOLO_FREQUENCY, LAVALINK_KEY_FILTER_VIBRATO, LAVALINK_KEY_FILTER_VIBRATO_DEPTH,
    LAVALINK_KEY_FILTER_VIBRATO_FREQUENCY, LAVALINK_KEY_FILTER_VOLUME
)

FILTER_IDENTIFIER_NONE = 0
FILTER_IDENTIFIER_EQUALIZER = 1
FILTER_IDENTIFIER_KARAOKE = 2
FILTER_IDENTIFIER_TIMESCALE = 3
FILTER_IDENTIFIER_TREMOLO = 4
FILTER_IDENTIFIER_VIBRATO = 5
FILTER_IDENTIFIER_ROTATION = 6
FILTER_IDENTIFIER_DISTORTION = 7
FILTER_IDENTIFIER_CHANNEL_MIX = 8
FILTER_IDENTIFIER_LOW_PASS = 9
FILTER_IDENTIFIER_VOLUME = 10

# Use these as references:
#
# https://github.com/freyacodes/Lavalink/blob/master/LavalinkServer/src/main/java/lavalink/server/player/filters/filterConfigs.kt
# https://github.com/freyacodes/Lavalink/blob/master/IMPLEMENTATION.md#using-filters
# https://github.com/natanbc/lavadsp/tree/master/src/main/java/com/github/natanbc/lavadsp

class Filter(RichAttributeErrorBaseType):
    """
    Represents filters applied to a solar client.
    
    Adding a filter can have adverse effects on performance. Filters force the lava player to decode all audio to PCM,
    even if the input was already in the Opus format that Discord uses. This means decoding and encoding audio that
    would normally require very little processing. This is often the case with YouTube videos.
    
    Class Attributes
    ----------------
    identifier : `int`
        The filter type's internal identifier.
    json_key : `str`
        The key of the filter used when serializing it.
    """
    identifier = FILTER_IDENTIFIER_NONE
    json_key = ''
    
    __slots__ = ()
    
    def __new__(cls):
        """
        Creates a new filter instance.
        """
        return object.__new__(cls)
    
    
    def __eq__(self, other):
        """Returns whether the two filters are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return True
    
    
    def __hash__(self):
        """Returns the filter's hash value."""
        return 0
    
    
    def __repr__(self):
        """Returns the filter's representation."""
        return f'<{self.__class__.__name__}>'
    
    
    def __bool__(self):
        """Returns whether the filter was changed."""
        return False
    
    
    def to_data(self):
        """
        Converts the filter to a json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `object`) items
        """
        return {}



class ChannelMix(Filter):
    """
    Mixes both channels (left and right), with a configurable factor on how much each channel affects the other.
    
    With the defaults, both channels are kept independent from each other.
    
    Setting all factors to 0.5 means both channels get the same audio.
    
    Attributes
    ----------
    _left_to_left : `float`
        Left-to-left factor.
    _left_to_right : `float`
        Left-to-right factor.
    _right_to_left : `float`
        Right-to-left factor.
    _right_to_right : `float`
        Right-to-right factor.
    
    Class Attributes
    ----------------
    identifier : `int`
        The filter type's internal identifier.
    json_key : `str`
        The key of the filter used when serializing it.
    """
    identifier = FILTER_IDENTIFIER_CHANNEL_MIX
    json_key = LAVALINK_KEY_FILTER_CHANNEL_MIX
    
    __slots__ = ('_left_to_left', '_left_to_right', '_right_to_left', '_right_to_right')
    
    def __new__(cls, left_to_left, left_to_right, right_to_right, right_to_left):
        """
        Creates a new channel mix filter.
        
        Parameters
        ----------
        left_to_left : `float`
            Left-to-left factor.
        left_to_right : `float`
            Left-to-right factor.
        right_to_right : `float`
            Right-to-right factor.
        right_to_left : `float`
            Right-to-left factor.
        
        Raises
        ------
        TypeError
            - If `left_to_left` is not `float`.
            - If `left_to_right` is not `float`.
            - If `right_to_right` is not `float`.
            - If `right_to_left` is not `float`.
        """
        if not isinstance(left_to_left, float):
            raise TypeError(
                f'`left_to_left` can be `float`, got {left_to_left.__class__.__name__}; {left_to_left!r}.'
            )
        
        if not isinstance(left_to_right, float):
            raise TypeError(
                f'`left_to_right` can be `float`, got {left_to_right.__class__.__name__}; {left_to_right!r}.'
            )
        
        if not isinstance(right_to_right, float):
            raise TypeError(
                f'`right_to_right` can be `float`, got {right_to_right.__class__.__name__}; {right_to_right!r}.'
            )
        
        if not isinstance(right_to_left, float):
            raise TypeError(
                f'`right_to_left` can be `float`, got {right_to_left.__class__.__name__}; {right_to_left!r}.'
            )
        
        
        self = object.__new__(cls)
        self._left_to_left = left_to_left
        self._left_to_right = left_to_right
        self._right_to_left = right_to_left
        self._right_to_right = right_to_right
        return self
    
    
    @copy_docs(Filter.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self._left_to_left != other._left_to_left:
            return False
        
        if self._left_to_right != other._left_to_right:
            return False
        
        if self._right_to_left != other._right_to_left:
            return False
        
        if self._right_to_right != other._right_to_right:
            return False
        
        return True
    
    
    @copy_docs(Filter.__hash__)
    def __hash__(self):
        hash_value = 0
        
        left_to_left = self._left_to_left
        if (left_to_left != 1.0):
            hash_value ^= (1 << 4)
            hash_value ^= hash(left_to_left)
        
        left_to_right = self._left_to_right
        if (left_to_right != 0.0):
            hash_value ^= (1 << 8)
            hash_value ^= hash(left_to_right)
        
        right_to_left = self._right_to_left
        if (right_to_left != 0.0):
            hash_value ^= (1 << 12)
            hash_value ^= hash(right_to_left)
        
        right_to_right = self._right_to_right
        if (right_to_right != 0.0):
            hash_value ^= (1 << 16)
            hash_value ^= hash(right_to_right)
        
        return hash_value
    
    
    @copy_docs(Filter.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' left_to_left = ')
        repr_parts.append(format(self._left_to_left, '.02f'))
        
        repr_parts.append(' left_to_right = ')
        repr_parts.append(format(self._left_to_right, '.02f'))
        
        repr_parts.append(' right_to_right = ')
        repr_parts.append(format(self._right_to_right, '.02f'))
        
        repr_parts.append(' right_to_left = ')
        repr_parts.append(format(self._right_to_left, '.02f'))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(Filter.__bool__)
    def __bool__(self):
        if self._left_to_left != 1.0:
            return True
        
        if self._left_to_right != 0.0:
            return True
        
        if self._right_to_right != 0.0:
            return True
        
        if self._right_to_left != 1.0:
            return True
        
        return False
    
    
    @copy_docs(Filter.to_data)
    def to_data(self):
        return {
            LAVALINK_KEY_FILTER_CHANNEL_MIX_LEFT_TO_LEFT: self._left_to_left,
            LAVALINK_KEY_FILTER_CHANNEL_MIX_LEFT_TO_RIGHT: self._left_to_right,
            LAVALINK_KEY_FILTER_CHANNEL_MIX_RIGHT_TO_LEFT: self._right_to_right,
            LAVALINK_KEY_FILTER_CHANNEL_MIX_RIGHT_TO_RIGHT: self._right_to_left,
        }


class Distortion(Filter):
    """
    Distortion effect.
    
    It can generate some pretty unique audio effects.
    
    Attributes
    ----------
    _cos_offset : `float`
        Cos offset.
    _cos_scale : `float`
        Cos scale.
    _offset : `float`
        Offset.
    _scale : `float`
        Scale.
    _sin_offset : `float`
        Sin offset.
    _sin_scale : `float`
        Sin scale.
    _tan_offset : `float`
        Tan offset.
    _tan_scale : `float`
        Tan scale.
    
    Class Attributes
    ----------------
    identifier : `int`
        The filter type's internal identifier.
    json_key : `str`
        The key of the filter used when serializing it.
    """
    identifier = FILTER_IDENTIFIER_DISTORTION
    json_key = LAVALINK_KEY_FILTER_DISTORTION
    
    __slots__ = (
        '_cos_offset', '_cos_scale', '_offset', '_scale', '_sin_offset', '_sin_scale', '_tan_offset', '_tan_scale'
    )
    
    def __new__(
        cls,
        *,
        sin_offset = 0.0,
        sin_scale = 1.0,
        cos_offset = 0.0,
        cos_scale = 1.0,
        tan_offset = 0.0,
        tan_scale = 1.0,
        offset = 0.0,
        scale = 1.0,
    ):
        """
        Creates a new distortion filter.
        
        Parameters
        ----------
        sin_offset : `float` = `0.0`, Optional (Keyword only)
            Sin offset.
        
        sin_scale : `float` = `1.0`, Optional (Keyword only)
            Sin scale.
        
        cos_offset : `float` = `0.0`, Optional (Keyword only)
            Cos offset.
        
        cos_scale : `float` = `1.0`, Optional (Keyword only)
            Cos scale.
        
        tan_offset : `float` = `0.0`, Optional (Keyword only)
            Tan offset.
        
        tan_scale : `float` = `1.0`, Optional (Keyword only)
            Tan scale.
            
        offset : `float` = `0.0`, Optional (Keyword only)
            Offset.
        
        scale : `float` = `1.0`, Optional (Keyword only)
            Scale.
        
        Raises
        ------
        TypeError
            - If `sin_offset` is not `float`.
            - If `sin_scale` is not `float`.
            - If `cos_offset` is not `float`.
            - If `cos_scale` is not `float`.
            - If `tan_offset` is not `float`.
            - If `tan_scale` is not `float`.
            - If `offset` is not `float`.
            - If `scale` is not `float`.
        """
        if not isinstance(sin_offset, float):
            raise TypeError(
                f'`sin_offset` can be `float`, got {sin_offset.__class__.__name__}; {sin_offset!r}.'
            )
        
        if not isinstance(sin_scale, float):
            raise TypeError(
                f'`sin_scale` can be `float`, got {sin_scale.__class__.__name__}; {sin_scale!r}.'
            )
        
        if not isinstance(cos_offset, float):
            raise TypeError(
                f'`cos_offset` can be `float`, got {cos_offset.__class__.__name__}; {cos_offset!r}.'
            )
        
        if not isinstance(cos_scale, float):
            raise TypeError(
                f'`cos_scale` can be `float`, got {cos_scale.__class__.__name__}; {cos_scale!r}.'
            )
        
        if not isinstance(tan_offset, float):
            raise TypeError(
                f'`tan_offset` can be `float`, got {tan_offset.__class__.__name__}; {tan_offset!r}.'
            )
        
        if not isinstance(tan_scale, float):
            raise TypeError(
                f'`tan_scale` can be `float`, got {tan_scale.__class__.__name__}; {tan_scale!r}.'
            )
        
        if not isinstance(offset, float):
            raise TypeError(
                f'`offset` can be `float`, got {offset.__class__.__name__}; {offset!r}.'
            )
        
        if not isinstance(scale, float):
            raise TypeError(
                f'`scale` can be `float`, got {scale.__class__.__name__}; {scale!r}.'
            )
        
        self = object.__new__(cls)
        self._cos_offset = cos_offset
        self._cos_scale = cos_scale
        self._offset = offset
        self._scale = scale
        self._sin_offset = sin_offset
        self._sin_scale = sin_scale
        self._tan_offset = tan_offset
        self._tan_scale = tan_scale
        return self
    
    
    @copy_docs(Filter.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self._cos_offset != other._cos_offset:
            return False
        
        if self._cos_scale != other._cos_scale:
            return False
        
        if self._offset != other._offset:
            return False
        
        if self._scale != other._scale:
            return False
        
        if self._sin_offset != other._sin_offset:
            return False
        
        if self._sin_scale != other._sin_scale:
            return False
        
        if self._tan_offset != other._tan_offset:
            return False
        
        if self._tan_scale != other._tan_scale:
            return False
        
        return True
    
    
    @copy_docs(Filter.__hash__)
    def __hash__(self):
        hash_value = 0
        
        cos_offset = self._cos_offset
        if (cos_offset != 0.0):
            hash_value ^= hash(cos_offset)
        
        cos_scale = self._cos_scale
        if (cos_scale != 1.0):
            hash_value ^= hash(cos_scale)
        
        offset = self._offset
        if (offset != 0.0):
            hash_value ^= hash(offset)
        
        scale = self._scale
        if (scale != 1.0):
            hash_value ^= hash(scale)
        
        sin_offset = self._sin_offset
        if (sin_offset != 0.0):
            hash_value ^= hash(sin_offset)
        
        sin_scale = self._sin_scale
        if (sin_scale != 1.0):
            hash_value ^= hash(sin_scale)
        
        tan_offset = self._tan_offset
        if (tan_offset != 0.0):
            hash_value ^= hash(tan_offset)
        
        tan_scale = self._tan_scale
        if (tan_scale != 1.0):
            hash_value ^= hash(tan_scale)
        
        return hash_value
    
    
    @copy_docs(Filter.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        sin_offset = self._sin_offset
        if (sin_offset != 0.0):
            field_added = True
        
            repr_parts.append(' sin_offset = ')
            repr_parts.append(format(sin_offset, '.02f'))
        
        else:
            field_added = False
        
        
        sin_scale = self._sin_scale
        if (sin_scale != 1.0):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' sin_scale = ')
            repr_parts.append(format(sin_scale, '.02f'))
        
        
        cos_offset = self._cos_offset
        if (cos_offset != 0.0):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' cos_offset = ')
            repr_parts.append(format(cos_offset, '.02f'))

        
        cos_scale = self._cos_scale
        if (cos_scale != 1.0):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' cos_scale = ')
            repr_parts.append(format(cos_scale, '.02f'))
        
        
        tan_offset = self._tan_offset
        if (tan_offset != 0.0):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' tan_offset = ')
            repr_parts.append(format(tan_offset, '.02f'))

        
        tan_scale = self._tan_scale
        if (tan_scale != 1.0):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' tan_scale = ')
            repr_parts.append(format(tan_scale, '.02f'))
        
        
        offset = self._offset
        if (offset != 0.0):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' offset = ')
            repr_parts.append(format(offset, '.02f'))

        
        scale = self._scale
        if (scale != 1.0):
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' scale = ')
            repr_parts.append(format(scale, '.02f'))
        
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(Filter.__bool__)
    def __bool__(self):
        if self._cos_offset != 0.0:
            return True
        
        if self._cos_scale != 1.0:
            return True
        
        if self._sin_offset == 0.0:
            return True
        
        if self._sin_scale != 1.0:
            return True
        
        if self._tan_offset == 0.0:
            return True
        
        if self._tan_scale != 1.0:
            return True
        
        if self._offset == 0.0:
            return True
        
        if self._scale != 1.0:
            return True
        
        return False
    
    
    @copy_docs(Filter.to_data)
    def to_data(self):
        return {
            LAVALINK_KEY_FILTER_DISTORTION_COS_OFFSET: self._cos_offset,
            LAVALINK_KEY_FILTER_DISTORTION_COS_SCALE: self._cos_scale,
            LAVALINK_KEY_FILTER_DISTORTION_SIN_OFFSET: self._sin_offset,
            LAVALINK_KEY_FILTER_DISTORTION_SIN_SCALE: self._sin_scale,
            LAVALINK_KEY_FILTER_DISTORTION_TAN_OFFSET: self._tan_offset,
            LAVALINK_KEY_FILTER_DISTORTION_TAN_SCALE: self._tan_scale,
            LAVALINK_KEY_FILTER_DISTORTION_OFFSET: self._offset,
            LAVALINK_KEY_FILTER_DISTORTION_SCALE: self._scale,
        }


class Equalizer(Filter):
    """
    There are 15 bands (0-14) that can be changed.
    
    "gain" is the multiplier for the given band. The default value is `0`. Valid values range from `-0.25` to `1.0`,
    where `-0.25` means the given band is completely muted, and `0.25` means it is doubled. Modifying the gain could
    also change the volume of the output.
    
    Attributes
    ----------
    _bands : `None` or `dict` of (`int`, `float`) items
        Bands.
    
    Class Attributes
    ----------------
    identifier : `int`
        The filter type's internal identifier.
    json_key : `str`
        The key of the filter used when serializing it.
    """
    identifier = FILTER_IDENTIFIER_EQUALIZER
    json_key = LAVALINK_KEY_FILTER_EQUALIZER
    
    __slots__ = ('_bands',)
    
    def __new__(cls, *band_gain_pairs):
        """
        Creates a new equalizer filter.
        
        Parameters
        ----------
        *band_gain_pairs : `tuple` (`int`, `float`)
            band-gain pairs.
        
        Raises
        ------
        TypeError
            If `band_gain_pairs` contains a non-tuple element.
        ValueError
            If a band is out of range [0:14].
        """
        bands = None
        
        for band_gain_pair in band_gain_pairs:
            if not isinstance(band_gain_pair, tuple):
                raise TypeError(
                    f'`band_gain_pairs` can contain `tuple` elements, got '
                    f'{band_gain_pair.__class__.__name__}; {band_gain_pair!r}; band_gain_pairs={band_gain_pairs!r}.'
                )
            
            band, gain = band_gain_pair
            
            if (band < 0) or (band >= LAVALINK_BAND_COUNT):
                raise ValueError(
                    f'`band`, can be in range [0:14], got {band!r}.'
                )
            
            if gain >= 1.0:
                gain = 1.0
            elif gain < -0.25:
                gain = -0.25
            elif gain == 0.0:
                continue
            
            if bands is None:
                bands = {}
            
            bands[band] = gain
        
        
        self = object.__new__(cls)
        self._bands = bands
        return self
    
    
    @copy_docs(Filter.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self._bands != other._bands:
            return False
        
        return True
    
    
    @copy_docs(Filter.__hash__)
    def __hash__(self):
        hash_value = 0
        
        bands = self._bands
        if (bands is not None):
            for item in bands.items():
                hash_value ^= hash(item)
        
        return hash_value
    
    
    @copy_docs(Filter.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        bands = self._bands
        if (bands is not None):
            repr_parts.append(' bands = {')
            field_added = False
            
            for band, gain in sorted(bands.items()):
                if field_added:
                    repr_parts.append(', ')
                else:
                    field_added = True
                
                repr_parts.append(repr(band))
                repr_parts.append(': ')
                repr_parts.append(repr(gain))
            
            repr_parts.append('}')
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(Filter.__bool__)
    def __bool__(self):
        if (self._bands is not None):
            return True
        
        return False
    
    
    @copy_docs(Filter.to_data)
    def to_data(self):
        bands = self._bands
        if (bands is None):
            return []
        
        return [
            {
                LAVALINK_KEY_FILTER_EQUALIZER_BAND: band,
                LAVALINK_KEY_FILTER_EQUALIZER_GAIN: gain,
            }
            for band, gain in self._bands.items()
        ]


class Karaoke(Filter):
    """
    Uses equalization to eliminate part of a band, usually targeting vocals.
    
    Attributes
    ----------
    _filter_band : `float`
        Filter band.
    _filter_width : `float`
        Filter width.
    _level : `float`
        Effect level.
    _mono_level : `float`
        Effect mono level.
    
    Class Attributes
    ----------------
    identifier : `int`
        The filter type's internal identifier.
    json_key : `str`
        The key of the filter used when serializing it.
    """
    identifier = FILTER_IDENTIFIER_KARAOKE
    json_key = LAVALINK_KEY_FILTER_KARAOKE
    
    __slots__ = ('_filter_band', '_filter_width', '_level', '_mono_level')
    
    def __new__(cls, *, filter_band = 220.0, filter_width = 100.0, level = 1.0, mono_level = 1.0):
        """
        Creates a new karaoke filter.
        
        Parameters
        ----------
        filter_band : `float` = `220.0`, Optional (Keyword only)
            Filter band.
            
        filter_width : `float` = `100.0`, Optional (Keyword only)
            Filter width.
        
        level : `float` = `1.0`, Optional (Keyword only)
            Effect level.
        
        mono_level : `float` = `1.0`, Optional (Keyword only)
            Effect mono level.
        
        Raises
        ------
        TypeError
            - If `level` is not `float`.
            - If `mono_level` is not `float`.
            - If `filter_band` is not `float`.
            - If `filter_width` is not `float`.
        """
        if not isinstance(level, float):
            raise TypeError(
                f'`level` can be `float`, got {level.__class__.__name__}; {level!r}.'
            )
        
        if not isinstance(mono_level, float):
            raise TypeError(
                f'`mono_level` can be `float`, got {mono_level.__class__.__name__}; {mono_level!r}.'
            )
        
        if not isinstance(filter_band, float):
            raise TypeError(
                f'`filter_band` can be `float`, got {filter_band.__class__.__name__}; {filter_band!r}.'
            )
        
        if not isinstance(filter_width, float):
            raise TypeError(
                f'`filter_width` can be `float`, got {filter_width.__class__.__name__}; {filter_width!r}.'
            )
        
        self = object.__new__(cls)
        self._filter_band = filter_band
        self._filter_width = filter_width
        self._level = level
        self._mono_level = mono_level
        return self
    
    
    @copy_docs(Filter.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self._filter_band != other._filter_band:
            return False
        
        if self._filter_width != other._filter_width:
            return False
        
        if self._level != other._level:
            return False
        
        if self._mono_level != other._mono_level:
            return False
        
        return True
    
    
    @copy_docs(Filter.__hash__)
    def __hash__(self):
        hash_value = 0
        hash_value ^= hash(self._filter_band)
        hash_value ^= hash(self._filter_width)
        hash_value ^= hash(self._level)
        hash_value ^= hash(self._mono_level)
        return hash_value
    
    
    @copy_docs(Filter.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' level = ')
        repr_parts.append(format(self._level, '.02f'))
        
        repr_parts.append(', mono_level = ')
        repr_parts.append(format(self._mono_level, '.02f'))
        
        repr_parts.append(', filter_band = ')
        repr_parts.append(format(self._filter_band, '.02f'))
        
        repr_parts.append(', filter_width = ')
        repr_parts.append(format(self._filter_width, '.02f'))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
        
    @copy_docs(Filter.__bool__)
    def __bool__(self):
        return True
    
    
    @copy_docs(Filter.to_data)
    def to_data(self):
        return {
            LAVALINK_KEY_FILTER_KARAOKE_FILTER_BAND: self._filter_band,
            LAVALINK_KEY_FILTER_KARAOKE_FILTER_WIDTH: self._filter_width,
            LAVALINK_KEY_FILTER_KARAOKE_LEVEL: self._level,
            LAVALINK_KEY_FILTER_KARAOKE_MONO_LEVEL: self._mono_level,
        }



class LowPass(Filter):
    """
    Higher frequencies get suppressed, while lower frequencies pass through this filter, thus the name low pass.
    
    Attributes
    ----------
    _smoothing : `float`
        Smoothing.
    
    Class Attributes
    ----------------
    identifier : `int`
        The filter type's internal identifier.
    json_key : `str`
        The key of the filter used when serializing it.
    """
    identifier = FILTER_IDENTIFIER_LOW_PASS
    json_key = LAVALINK_KEY_FILTER_LOW_PASS
    
    __slots__ = ('_smoothing',)
    
    def __new__(cls, smoothing):
        """
        Creates a new low pass filter.
        
        Parameters
        ----------
        smoothing : `float`
            Smoothing.
        
        Raises
        ------
        TypeError
            - If `smoothing` is not `float`.
        """
        if not isinstance(smoothing, float):
            raise TypeError(
                f'`smoothing` can be `float`, got {smoothing.__class__.__name__}; {smoothing!r}.'
            )
        
        
        self = object.__new__(cls)
        self._smoothing = smoothing
        return self
    
    
    @copy_docs(Filter.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self._smoothing != other._smoothing:
            return False
        
        return True
    
    
    @copy_docs(Filter.__hash__)
    def __hash__(self):
        hash_value = 0
        
        smoothing = self._smoothing
        if (smoothing != 20.0):
            hash_value ^= hash(smoothing)
        
        
        return hash_value
    
    
    @copy_docs(Filter.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' smoothing = ')
        repr_parts.append(format(self._smoothing, '.02f'))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(Filter.__bool__)
    def __bool__(self):
        if self._smoothing != 20.0:
            return True
        
        return False
    
    
    @copy_docs(Filter.to_data)
    def to_data(self):
        return {
            LAVALINK_KEY_FILTER_LOW_PASS_SMOOTHING: self._smoothing,
        }



class Rotation(Filter):
    """
    Rotates the sound around the stereo channels/user headphones aka Audio Panning.
    
    It can produce an effect similar to: ``this:https://youtu.be/QB9EB8mTKcc`` (without the reverb).
    
    Attributes
    ----------
    _rotation : `float`
        The frequency of the audio rotating around the listener in seconds.
        
        > 0.2 is similar to the example video above.
    
    Class Attributes
    ----------------
    identifier : `int`
        The filter type's internal identifier.
    json_key : `str`
        The key of the filter used when serializing it.
    """
    identifier = FILTER_IDENTIFIER_ROTATION
    json_key = LAVALINK_KEY_FILTER_ROTATION
    
    __slots__ = ('_rotation',)
    
    def __new__(cls, rotation):
        """
        Creates a new rotation filter.
        
        Parameters
        ----------
        rotation : `float`
            The frequency of the audio rotating around the listener in Hz.
        
        Raises
        ------
        TypeError
            - If `rotation` is not `float`.
            
        """
        if not isinstance(rotation, float):
            raise TypeError(
                f'`rotation` can be `float`, got {rotation.__class__.__name__}; {rotation!r}.'
            )
        
        
        self = object.__new__(cls)
        self._rotation = rotation
        return self
    
    
    @copy_docs(Filter.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self._rotation != other._rotation:
            return False
        
        return True
    
    
    @copy_docs(Filter.__hash__)
    def __hash__(self):
        hash_value = 0
        
        rotation = self._rotation
        if (rotation != 0.0):
            hash_value ^= hash(rotation)
        
        
        return hash_value
    
    
    @copy_docs(Filter.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' rotation = ')
        repr_parts.append(format(self._rotation, '.02f'))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(Filter.__bool__)
    def __bool__(self):
        if self._rotation != 0.0:
            return True
        
        return False
    
    
    @copy_docs(Filter.to_data)
    def to_data(self):
        return {
            LAVALINK_KEY_FILTER_ROTATION_ROTATION: self._rotation,
        }


class Timescale(Filter):
    """
    Changes the speed, pitch, and rate. All default to 1.
    
    Attributes
    ----------
    _pitch : `float`
        Audio pitch.
    _rate : `float`
        Playback rate.
    _speed : `float`
        Playback speed.
    
    Class Attributes
    ----------------
    identifier : `int`
        The filter type's internal identifier.
    json_key : `str`
        The key of the filter used when serializing it.
    """
    identifier = FILTER_IDENTIFIER_TIMESCALE
    json_key = LAVALINK_KEY_FILTER_TIMESCALE
    
    __slots__ = ('_pitch', '_rate', '_speed')
    
    def __new__(cls, *, pitch = 1.0, rate = 1.0, speed = 1.0):
        """
        Creates a new timescale filter.
        
        Parameters
        ----------
        pitch : `float` = `1.0`, Optional (Keyword only):
            Audio pitch.
        
        rate : `float` = `1.0`, Optional (Keyword only):
            Playback rate.
        
        speed : `float` = `1.0`, Optional (Keyword only)
            Playback speed.
        
        Raises
        ------
        TypeError
            - If `speed` is not `float`.
            - If `pitch` is not `float`.
            - If `rate` is not `float`.
        """
        if not isinstance(speed, float):
            raise TypeError(
                f'`speed` can be `float`, got {speed.__class__.__name__}; {speed!r}.'
            )
        
        if not isinstance(pitch, float):
            raise TypeError(
                f'`pitch` can be `float`, got {pitch.__class__.__name__}; {pitch!r}.'
            )
        
        if not isinstance(rate, float):
            raise TypeError(
                f'`rate` can be `float`, got {rate.__class__.__name__}; {rate!r}.'
            )
        
        if speed < 0:
            raise ValueError(
                f'`speed`, can be in range [0:], got {speed!r}.'
            )
        
        if pitch < 0:
            raise ValueError(
                f'`pitch`, can be in range [0:], got {pitch!r}.'
            )
        
        if rate < 0:
            raise ValueError(
                f'`rate`, can be in range [0:], got {rate!r}.'
            )
        
        self = object.__new__(cls)
        self._pitch = pitch
        self._rate = rate
        self._speed = speed
        return self
    
    
    @copy_docs(Filter.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self._pitch != other._pitch:
            return False
        
        if self._rate != other._rate:
            return False
        
        if self._speed != other._speed:
            return False
        
        return True
    
    
    @copy_docs(Filter.__hash__)
    def __hash__(self):
        hash_value = 0
        
        pitch = self._pitch
        if (pitch != 1.0):
            hash_value ^= hash(pitch)
        
        rate = self._rate
        if (rate != 1.0):
            hash_value ^= hash(rate)
        
        speed = self._speed
        if (speed != 1.0):
            hash_value ^= hash(speed)
        
        return hash_value
    
    
    @copy_docs(Filter.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        speed = self._speed
        if (speed != 1.0):
            field_added = True
            
            repr_parts.append(' speed = ')
            repr_parts.append(format(speed, '.02f'))
        
        else:
            field_added = False
        
        pitch = self._pitch
        if (pitch != 1.0):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            repr_parts.append(' pitch = ')
            repr_parts.append(format(pitch, '.02f'))
        
        rate = self._rate
        if (rate != 1.0):
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' rate = ')
            repr_parts.append(format(rate, '.02f'))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(Filter.__bool__)
    def __bool__(self):
        if self._pitch != 1.0:
            return True
        
        if self._rate != 1.0:
            return True
        
        if self._speed != 1.0:
            return True
        
        return False
    
    
    @copy_docs(Filter.to_data)
    def to_data(self):
        return {
            LAVALINK_KEY_FILTER_TIMESCALE_PITCH: self._pitch,
            LAVALINK_KEY_FILTER_TIMESCALE_RATE: self._rate,
            LAVALINK_KEY_FILTER_TIMESCALE_SPEED: self._speed,
        }
    


class Tremolo(Filter):
    """
    Uses amplification to create a shuddering effect, where the volume quickly oscillates.
    
    Example ``here:https://en.wikipedia.org/wiki/File:Fuse_Electronics_Tremolo_MK-III_Quick_Demo.ogv``.
    
    Attributes
    ----------
    _depth : `float`
        Effect depth.
    _frequency : `float`
        Effect frequency.
    
    Class Attributes
    ----------------
    identifier : `int`
        The filter type's internal identifier.
    json_key : `str`
        The key of the filter used when serializing it.
    """
    identifier = FILTER_IDENTIFIER_TREMOLO
    json_key = LAVALINK_KEY_FILTER_TREMOLO
    
    __slots__ = ('_depth', '_frequency')
    
    def __new__(cls, frequency, depth):
        """
        Creates a new tremolo filter.
        
        Parameters
        ----------
        frequency : `float`
            Effect frequency.
        depth : `float`
            Effect depth.
        
        Raises
        ------
        TypeError
            - If `frequency` is not `float`.
            - If `depth` is not `float`.
        ValueError
            - If `frequency` is out of `(0.0:)`.
            - If `depth` is out of `(0.0:1.0]`.
            
        """
        if not isinstance(frequency, float):
            raise TypeError(
                f'`frequency` can be `float`, got {frequency.__class__.__name__}; {frequency!r}.'
            )
        
        if not isinstance(depth, float):
            raise TypeError(
                f'`depth` can be `float`, got {depth.__class__.__name__}; {depth!r}.'
            )
        
        
        if frequency <= 0.0:
            raise ValueError(
                f'`frequency` can be in range `(0.0:)`, got {frequency!r}.'
        )
        
        
        if (depth <= 0.0) or (depth > 1.0):
            raise ValueError(
                f'`depth` can be in range `(0.0:1.0]`, got {depth!r}.'
        )
        
        
        self = object.__new__(cls)
        self._depth = depth
        self._frequency = frequency
        return self
    
    
    @copy_docs(Filter.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self._depth != other._depth:
            return False
        
        if self._frequency != other._frequency:
            return False
        
        return True
    
    
    @copy_docs(Filter.__hash__)
    def __hash__(self):
        hash_value = 0
        
        depth = self._depth
        if (depth != 0.0):
            hash_value ^= hash(depth)
        
        hash_value ^= hash(self._frequency)
        
        return hash_value
    
    
    @copy_docs(Filter.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' depth = ')
        repr_parts.append(format(self._depth, '.02f'))
        
        repr_parts.append(', frequency = ')
        repr_parts.append(format(self._frequency, '.02f'))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(Filter.__bool__)
    def __bool__(self):
        if self._depth != 0.0:
            return True
        
        return False
    
    
    @copy_docs(Filter.to_data)
    def to_data(self):
        return {
            LAVALINK_KEY_FILTER_TREMOLO_DEPTH: self._depth,
            LAVALINK_KEY_FILTER_TREMOLO_FREQUENCY: self._frequency,
        }


class Vibrato(Filter):
    """
    Similar to tremolo. While tremolo oscillates the volume, vibrato oscillates the pitch.
    
    Attributes
    ----------
    _depth : `float`
        Effect depth.
    _frequency : `float`
        Effect frequency.
    
    Class Attributes
    ----------------
    identifier : `int`
        The filter type's internal identifier.
    json_key : `str`
        The key of the filter used when serializing it.
    """
    identifier = FILTER_IDENTIFIER_VIBRATO
    json_key = LAVALINK_KEY_FILTER_VIBRATO
    
    __slots__ = ('_depth', '_frequency')
    
    def __new__(cls, frequency, depth):
        """
        Creates a new vibrato filter.
        
        Parameters
        ----------
        frequency : `float`
            Effect frequency.
        depth : `float`
            Effect depth.
        
        Raises
        ------
        TypeError
            - If `frequency` is not `float`.
            - If `depth` is not `float`.
        ValueError
            - If `frequency` is out of `(0.0:14.0]`.
            - If `depth` is out of `(0.0:1.0]`.
            
        """
        if not isinstance(frequency, float):
            raise TypeError(
                f'`frequency` can be `float`, got {frequency.__class__.__name__}; {frequency!r}.'
            )
        
        if not isinstance(depth, float):
            raise TypeError(
                f'`depth` can be `float`, got {depth.__class__.__name__}; {depth!r}.'
            )
        
        
        if (frequency <= 0.0) or (frequency > 14.0):
            raise ValueError(
                f'`frequency` can be in range `(0.0:14.0]`, got {frequency!r}.'
        )
        
        
        if (depth <= 0.0) or (depth > 1.0):
            raise ValueError(
                f'`depth` can be in range `(0.0:1.0]`, got {depth!r}.'
        )
        
        
        self = object.__new__(cls)
        self._depth = depth
        self._frequency = frequency
        return self
    
    
    @copy_docs(Filter.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self._depth != other._depth:
            return False
        
        if self._frequency != other._frequency:
            return False
        
        return True
    
    
    @copy_docs(Filter.__hash__)
    def __hash__(self):
        hash_value = 0
        
        depth = self._depth
        if (depth != 0.0):
            hash_value ^= hash(depth)
        
        hash_value ^= hash(self._frequency)
        
        return hash_value
    
    
    @copy_docs(Filter.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' depth = ')
        repr_parts.append(format(self._depth, '.02f'))
        
        repr_parts.append(', frequency = ')
        repr_parts.append(format(self._frequency, '.02f'))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(Filter.__bool__)
    def __bool__(self):
        if self._depth != 0.0:
            return True
        
        return False
    
    
    @copy_docs(Filter.to_data)
    def to_data(self):
        return {
            LAVALINK_KEY_FILTER_VIBRATO_DEPTH: self._depth,
            LAVALINK_KEY_FILTER_VIBRATO_FREQUENCY: self._frequency,
        }



class Volume(Filter):
    """
    Float value where `1.0` is 100%.
    
    Values `> 1.0` may cause clipping.
    
    Attributes
    ----------
    _volume : `float`
        The volume to set.
    
    Class Attributes
    ----------------
    identifier : `int`
        The filter type's internal identifier.
    json_key : `str`
        The key of the filter used when serializing it.
    """
    identifier = FILTER_IDENTIFIER_VOLUME
    json_key = LAVALINK_KEY_FILTER_VOLUME
    
    __slots__ = ('_volume',)
    
    def __new__(cls, volume):
        """
        Creates a new volume filter.
        
        Parameters
        ----------
        volume : `float`
        The volume to set.
        
        Raises
        ------
        TypeError
            - If `volume` is not `float`.
        ValueError
            - If volume is over `5`.
        """
        if not isinstance(volume, float):
            raise TypeError(
                f'`volume` can be `float`, got {volume.__class__.__name__}; {volume!r}.'
            )
        
        if volume > 5.0:
            raise ValueError(
                f'`volume` can be in range `[0.0:5.0]`, got {volume!r}.'
        )
        
        self = object.__new__(cls)
        self._volume = volume
        return self
    
    
    @copy_docs(Filter.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        if self._volume != other._volume:
            return False
        
        return True
    
    
    @copy_docs(Filter.__hash__)
    def __hash__(self):
        return hash(self._volume)
    
    
    @copy_docs(Filter.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__]
        
        repr_parts.append(' volume = ')
        repr_parts.append(format(self._volume, '.02f'))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(Filter.__bool__)
    def __bool__(self):
        if self._volume != 1.0:
            return True
        
        return False
    
    
    @copy_docs(Filter.to_data)
    def to_data(self):
        return self._volume
