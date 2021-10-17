__all__ = ('Track', )

from math import floor
from base64 import b64decode

from ...backend.utils import un_map_pack

from .constants import LAVALINK_KEY_TRACK, LAVALINK_KEY_START_TIME, LAVALINK_KEY_END_TIME, LAVALINK_KEY_TRACK_BASE64, \
    LAVALINK_KEY_TRACK_DICT, LAVALINK_KEY_TRACK_IDENTIFIER, LAVALINK_KEY_TRACK_SEEKABLE, LAVALINK_KEY_TRACK_AUTHOR, \
    LAVALINK_KEY_TRACK_DURATION_MS, LAVALINK_KEY_TRACK_IS_STREAM, LAVALINK_KEY_TRACK_TITLE, \
    LAVALINK_KEY_TRACK_URL, LAVALINK_KEY_TRACK_POSITION_MS

def _iter_configured_track_attributes(configured_track):
    """
    Yields `key` - `value` pairs of a configured track.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    configured_track : ``ConfiguredTrack``
        The configured pack to deserialize.
    
    Yields
    ------
    key : `str`
    value : `Any`
    """
    yield LAVALINK_KEY_TRACK, configured_track.track.base64
    
    start_time = configured_track.start_time
    if start_time:
        yield LAVALINK_KEY_START_TIME, floor(start_time*1000.0)
    
    end_time = configured_track.end_time
    if end_time:
        yield LAVALINK_KEY_END_TIME, floor(end_time*1000.0)


class Track:
    """
    Represents an audio track sent by lavalink.
    
    Parameters
    ----------
    author : `str`
        The track's uploader.
    base64 : `str`
        The base 64 version of the track.
    duration : `float`
        The duration of the track in seconds.
    identifier : `str`
        The track's identifier.
    is_stream : `bool`
        Whether the track is a live-stream.
    is_seekable : `bool`
        Whether the track supports seeking.
    position : `float`
        The position of the track in seconds.
    title : `str`
        The track's title.
    url : `None` or `str`
        The url of the track.
    """
    __slots__ = ('author', 'base64', 'duration', 'identifier', 'is_seekable', 'is_stream', 'position', 'title', 'url')
    
    def __new__(cls, data):
        """
        Creates a new track from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Track data.
        """
        self = object.__new__(cls)
        self.base64 = data[LAVALINK_KEY_TRACK_BASE64]
        
        track_data = data[LAVALINK_KEY_TRACK_DICT]
        
        self.author = track_data[LAVALINK_KEY_TRACK_AUTHOR]
        self.duration = track_data[LAVALINK_KEY_TRACK_DURATION_MS]*0.001
        self.identifier = track_data[LAVALINK_KEY_TRACK_IDENTIFIER]
        self.is_stream = track_data[LAVALINK_KEY_TRACK_IS_STREAM]
        self.is_seekable = track_data[LAVALINK_KEY_TRACK_SEEKABLE]
        self.title = track_data[LAVALINK_KEY_TRACK_TITLE]
        self.url = track_data[LAVALINK_KEY_TRACK_URL]
        
        try:
            position = track_data[LAVALINK_KEY_TRACK_POSITION_MS]
        except KeyError:
            position = 0.0
        else:
            position *= 0.001
        self.position = position
        
        return self
    
    @classmethod
    def from_base64(cls, base64):
        """
        Creates a new track from base 64 data.
        
        Parameters
        ----------
        base64 : `str`
            Track data in base 64.
        
        Returns
        -------
        
        """
        data = b64decode(base64)
        
        # read flags
        
        flags = int.from_bytes(data[0:4], 'big')
        flags = (flags & 0xC0000000) >> 30
        
        # read version
        
        if flags&1:
            version = data[4]
            cursor_start = 5
        else:
            version = 1
            cursor_start = 4
        
        # read title
        
        cursor_end = cursor_start+2
        title_length = int.from_bytes(data[cursor_start:cursor_end], 'big')
        
        cursor_start = cursor_end
        cursor_end = cursor_start + title_length
        title = data[cursor_start:cursor_end]
        title = title.decode(errors='ignore')
        
        # read author
        
        cursor_start = cursor_end
        cursor_end = cursor_start + 2
        author_length = int.from_bytes(data[cursor_start:cursor_end], 'big')
        
        cursor_start = cursor_end
        cursor_end = cursor_start + author_length
        author = data[cursor_start:cursor_end]
        author = author.decode()
        
        # read duration
        
        cursor_start = cursor_end
        cursor_end = cursor_start + 8
        duration = int.from_bytes(data[cursor_start:cursor_end], 'big')
        duration *= 0.001
        
        # read identifier
        
        cursor_start = cursor_end
        cursor_end = cursor_start + 2
        identifier_length = int.from_bytes(data[cursor_start:cursor_end], 'big')
        
        cursor_start = cursor_end
        cursor_end = cursor_start + identifier_length
        identifier = data[cursor_start:cursor_end]
        identifier = identifier.decode()
        
        # read is_stream
        
        if data[cursor_end]:
            is_stream = True
        else:
            is_stream = False
        cursor_end += 1
        
        # read url
        
        if data[cursor_end]:
            cursor_start = cursor_end+1
            cursor_end = cursor_start+2
            
            url_length = int.from_bytes(data[cursor_start:cursor_end], 'big')
            
            cursor_start = cursor_end
            cursor_end = cursor_start + url_length
            url = data[cursor_start:cursor_end]
            url = url.decode()
            
        else:
            cursor_end += 1
            url = None
        
        # read source
        
        cursor_start = cursor_end
        cursor_end = cursor_start + 2
        source_length = int.from_bytes(data[cursor_start:cursor_end], 'big')
        
        cursor_start = cursor_end
        cursor_end = cursor_start + source_length
        source = data[cursor_start:cursor_end]
        source = source.decode()
        
        # read position
        
        cursor_start = cursor_end
        cursor_end = cursor_start + 8
        position = int.from_bytes(data[cursor_start:cursor_end], 'big')
        position *= 0.001
        
        self = object.__new__(cls)
        
        self.base64 = base64
        self.author = author
        self.duration = duration
        self.identifier = identifier
        self.is_stream = is_stream
        self.is_seekable = (not is_stream)
        self.title = title
        self.url = url
        self.position = position
        
        return self
    
    
    def __repr__(self):
        """Returns the track's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        
        if self.is_stream:
            field_added = False
            repr_parts.append(' stream')
        else:
            field_added = True
        
        if self.is_seekable:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' seekable')
        
        if not field_added:
            repr_parts.append(',')
        
        repr_parts.append(' author=')
        repr_parts.append(repr(self.author))
        
        repr_parts.append(', duration=')
        repr_parts.append(self.duration.__format__('.03f'))
        repr_parts.append('s')
        
        position = self.position
        if position:
            repr_parts.append(', position=')
            repr_parts.append(position.__format__('.03f'))
            repr_parts.append('s')
        
        repr_parts.append(', identifier=')
        repr_parts.append(repr(self.identifier))
        
        repr_parts.append(', title=')
        repr_parts.append(repr(self.title))
        
        url = self.url
        if (url is not None):
            repr_parts.append(', url=')
            repr_parts.append(repr(url))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)


class ConfiguredTrack:
    __slots__ = ('_added_attributes', 'end_time', 'start_time', 'track')
    
    def __new__(cls, track, start_time, end_time, added_attributes):
        """
        Creates a new configured track from the given parameters.
        
        Parameters
        ----------
        track : ``Track``
            The wrapped track.
        start_time : `float`
            Where the track will start in seconds.
        end_time : `float`
            Where the track will start in seconds.
        added_attributes : `dict` of (`str`, `Any`)
            Additional user defined attributes.
        
        Raises
        ------
        ValueError
            - If `start_time` is out of the expected [0.0:duration] range.
            - If `end_time` is out of the expected [0.0:duration] range.
        """
        duration = track.duration
        if start_time:
            if (start_time < 0.0) or (start_time > duration):
                raise ValueError(f'`start_time` can be in range [0.0:{duration:.3f}], got {end_time:.3f}.')
        
        if end_time:
            if (end_time < 0.0) or (end_time > duration):
                raise ValueError(f'`end_time` can be in range [0.0:{duration:.3f}], got {end_time:.3f}.')
        
        if not added_attributes:
            added_attributes = None
        
        self = object.__new__(cls)
        self.track = track
        self.start_time = start_time
        self.end_time = end_time
        self._added_attributes = added_attributes
    
        return self
    
    def __getattr__(self, attribute_name):
        """Tries to find the attributes from the added attributes."""
        added_attributes = self._added_attributes
        if (added_attributes is not None):
            try:
                return added_attributes[attribute_name]
            except KeyError:
                pass
        
        raise AttributeError(attribute_name)
    
    def un_pack(self):
        """
        Unpacks the configured track to `key` - `value` pairs accepted by lavalink.
        
        Returns
        -------
        un_map_packer : ``un_map_pack``
        """
        return un_map_pack(_iter_configured_track_attributes(self))
    
    
    def __repr__(self):
        """Returns the configured track's representation."""
        repr_parts = [
            '<', self.__class__.__name__,
            ' track=', repr(self.track),
        ]
        
        start_time = self.start_time
        if start_time:
            repr_parts.append(', start_time=')
            repr_parts.append(start_time.__format__('.3f'))
            repr_parts.append('s')
        
        end_time = self.end_time
        if end_time:
            repr_parts.append(', end_time=')
            repr_parts.append(end_time.__format__('.3f'))
            repr_parts.append('s')
        
        added_attributes = self._added_attributes
        if (added_attributes is not None):
            for attribute_name, attribute_value in added_attributes:
                repr_parts.append(', ')
                repr_parts.append(attribute_name)
                repr_parts.append(repr(attribute_value))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
