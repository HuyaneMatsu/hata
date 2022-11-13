__all__ = ('GetTracksResult', 'Track', )

from base64 import b64decode
from math import floor

from scarletio import RichAttributeErrorBaseType, un_map_pack

from .constants import (
    LAVALINK_KEY_END_TIME, LAVALINK_KEY_PLAYLIST, LAVALINK_KEY_PLAYLIST_NAME,
    LAVALINK_KEY_PLAYLIST_SELECTED_TRACK_INDEX, LAVALINK_KEY_START_TIME, LAVALINK_KEY_TRACK, LAVALINK_KEY_TRACKS,
    LAVALINK_KEY_TRACK_AUTHOR, LAVALINK_KEY_TRACK_BASE64, LAVALINK_KEY_TRACK_DICT, LAVALINK_KEY_TRACK_DURATION_MS,
    LAVALINK_KEY_TRACK_IDENTIFIER, LAVALINK_KEY_TRACK_IS_STREAM, LAVALINK_KEY_TRACK_POSITION_MS,
    LAVALINK_KEY_TRACK_SEEKABLE, LAVALINK_KEY_TRACK_TITLE, LAVALINK_KEY_TRACK_URL
)


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
        yield LAVALINK_KEY_START_TIME, floor(start_time * 1000.0)
    
    end_time = configured_track.end_time
    if end_time:
        yield LAVALINK_KEY_END_TIME, floor(end_time * 1000.0)


class Track(RichAttributeErrorBaseType):
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
    url : `None`, `str`
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
            Track data in base64.
        """
        data = b64decode(base64)
        
        # read flags
        
        flags = int.from_bytes(data[0:4], 'big')
        flags = (flags & 0xC0000000) >> 30
        
        # read version
        
        if flags & 1:
            version = data[4]
            cursor_start = 5
        else:
            version = 1
            cursor_start = 4
        
        # read title
        
        cursor_end = cursor_start + 2
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
        author = author.decode(errors='ignore')
        
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
            cursor_start = cursor_end + 1
            cursor_end = cursor_start + 2
            
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
            field_added = True
            repr_parts.append(' stream')
        else:
            field_added = False
        
        if self.is_seekable:
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' seekable')
        
        if not field_added:
            repr_parts.append(',')
        
        repr_parts.append(' author = ')
        repr_parts.append(repr(self.author))
        
        repr_parts.append(', duration = ')
        repr_parts.append(self.duration.__format__('.03f'))
        repr_parts.append('s')
        
        position = self.position
        if position:
            repr_parts.append(', position = ')
            repr_parts.append(position.__format__('.03f'))
            repr_parts.append('s')
        
        repr_parts.append(', identifier = ')
        repr_parts.append(repr(self.identifier))
        
        repr_parts.append(', title = ')
        repr_parts.append(repr(self.title))
        
        url = self.url
        if (url is not None):
            repr_parts.append(', url = ')
            repr_parts.append(repr(url))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the track's hash."""
        return hash(self.base64)
    
    
    def __eq__(self, other):
        """Returns whether the two tracks are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.base64 == other.base64:
            return True
        
        return False


class ConfiguredTrack(RichAttributeErrorBaseType):
    """
    Represents a track added to a player. Not like generic tracks, this supports additional attributes as well.
    
    Attributes
    ----------
    _added_attributes : `None`, `dict` of (`str`, `Any`) items
        Additionally passed attributes when registering a track.
    
    end_time : `float`
        When the track will end.
        
        Defaults to `0.0`.
    
    start_time : `float`
        When the track will start.
        
        Defaults to `0.0`.
    
    track : ``Track``
        The source track.
    """
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
        TypeError
            If `track` is neither ``Track``, nor ``ConfiguredTrack``.
        ValueError
            - If `start_time` is out of the expected [0.0:duration] range.
            - If `end_time` is out of the expected [0.0:duration] range.
        """
        if isinstance(track, Track):
            configuration = None
        elif isinstance(track, ConfiguredTrack):
            configuration = track
            track = track.track
        else:
            raise TypeError(
                f'`track` can be `{Track.__name__}`, `{ConfiguredTrack.__name__}`, got '
                f'{track.__class__.__name__}; {track!r}.'
            )
        
        duration = track.duration
        if start_time:
            if (start_time < 0.0) or (start_time > duration):
                raise ValueError(
                    f'`start_time` can be in range [0.0:{duration:.3f}], got {end_time:.3f}.'
                )
        else:
            if (configuration is not None):
                start_time = configuration.start_time
        
        if end_time:
            if (end_time < 0.0) or (end_time > duration):
                raise ValueError(
                    f'`end_time` can be in range [0.0:{duration:.3f}], got {end_time:.3f}.'
                )
        else:
            if (configuration is not None):
                start_time = configuration.end_time
        
        if added_attributes:
            if (configuration is not None):
                configuration_added_attributes = configuration._added_attributes
                if (configuration_added_attributes is not None):
                    added_attributes = {**configuration_added_attributes, **added_attributes}
        else:
            if (configuration is None):
                added_attributes = None
            else:
                added_attributes = configuration._added_attributes
                if (added_attributes is not None):
                    added_attributes = added_attributes.copy()
        
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
        
        RichAttributeErrorBaseType.__getattr__(self, attribute_name)
    
    
    def __dir__(self):
        """Returns the attribute names of the object."""
        directory = set(object.__dir__(self))
        added_attributes = self._added_attributes
        if (added_attributes is not None):
            directory.update(added_attributes.keys())
        
        return sorted(directory)
    
    
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
            for attribute_name, attribute_value in added_attributes.items():
                repr_parts.append(', ')
                repr_parts.append(attribute_name)
                repr_parts.append('=')
                repr_parts.append(repr(attribute_value))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the configured track's hash value."""
        hash_value = 0
        
        start_time = self.start_time
        if start_time:
            hash_value ^= (1 << 7)
            hash_value ^= hash(start_time)
        
        end_time = self.end_time
        if end_time:
            hash_value ^= (1 << 14)
            hash_value ^= hash(end_time)
        
        hash_value ^= hash(self.track)
        
        added_attributes = self.added_attributes
        if (added_attributes is not None):
            hash_value ^= len(added_attributes)
            
            for item in added_attributes.items():
                hash_value ^= hash(item)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two configured tracks are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.track != other.track:
            return False
        
        if self.end_time != other.end_time:
            return False
        
        if self.start_time != other.start_time:
            return False
        
        if self._added_attributes != other._added_attributes:
            return False
        
        return True
    
    
    @property
    def author(self):
        """
        Returns the track's uploader.
        
        Returns
        -------
        author : `str`
        """
        return self.track.author
    
    
    @property
    def base64(self):
        """
        Returns the track's base 64 version.
        
        Returns
        -------
        base64 : `str`
        """
        return self.track.base64
    
    
    @property
    def duration(self):
        """
        Returns the track's duration in seconds.
        
        Returns
        -------
        duration : `float`
        """
        return self.track.duration
    
    
    @property
    def identifier(self):
        """
        Returns the track's identifier.
        
        Returns
        -------
        identifier : `str`
        """
        return self.track.identifier
    
    
    @property
    def is_stream(self):
        """
        Returns whether the track is a live-stream.
        
        Returns
        -------
        is_stream : `bool`
        """
        return self.track.is_stream
    
    
    @property
    def is_seekable(self):
        """
        Returns whether the track supports seeking.
        
        Returns
        -------
        is_seekable : `bool`
        """
        return self.track.is_seekable
    
    
    @property
    def position(self):
        """
        Returns the position of the track.
        
        Returns
        -------
        position : `float`
        """
        return self.track.position
    
    
    @property
    def title(self):
        """
        Returns the track's title.
        
        Returns
        -------
        title : `str`
        """
        return self.track.title
    
    
    @property
    def url(self):
        """
        Returns the track's url.
        
        Returns
        -------
        url : `None`, `str`
        """
        return self.track.url
    
    
    def copy(self):
        """
        Copies the configured track.
        
        Returns
        -------
        new : ``ConfiguredTrack``
        """
        added_attributes = self._added_attributes
        if (added_attributes is not None):
            added_attributes = added_attributes.copy()
        
        new = object.__new__(type(self))
        
        new._added_attributes = added_attributes
        new.end_time = self.end_time
        new.start_time = self.start_time
        new.track = self.track
        
        return new


class GetTracksResult(RichAttributeErrorBaseType):
    """
    Returned by ``SolarClient.get_tracks`` if the request succeeded.
    
    Attributes
    ----------
    playlist_name : `None`, `str`
        The playlist's name, of what the tracks are part.
        
        Defaults to `None`.
        
    selected_track_index : `int`
        The selected track's index inside of the playlist.
        
        Defaults to `-1`.
    
    tracks : `None`, `tuple` of ``Track``
        The matched tracks.
        
        Defaults to `None`.
    """
    __slots__ = ('playlist_name', 'selected_track_index', 'tracks',)
    
    def __new__(cls, data):
        """
        Creates a new get tracks result instance from the given response data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Response data.
        """
        playlist_data = data[LAVALINK_KEY_PLAYLIST]
        if playlist_data is None:
            playlist_name = None
            selected_track_index = -1
        else:
            playlist_name = playlist_data.get(LAVALINK_KEY_PLAYLIST_NAME, None)
            selected_track_index = playlist_data.get(LAVALINK_KEY_PLAYLIST_SELECTED_TRACK_INDEX, -1)
        
        track_datas = data[LAVALINK_KEY_TRACKS]
        if (track_datas is None) or (not track_datas):
            tracks = None
        else:
            tracks = tuple(Track(track_data) for track_data in track_datas)
        
        self = object.__new__(cls)
        self.playlist_name = playlist_name
        self.selected_track_index = selected_track_index
        self.tracks = tracks
        return self
    
    
    def __repr__(self):
        """Returns the get tracks result's representation."""
        repr_parts = ['<', self.__class__.__name__]
        
        playlist_name = self.playlist_name
        if (playlist_name is None):
            field_added = False
        else:
            field_added = True
            
            repr_parts.append(' playlist_name=')
            repr_parts.append(repr(playlist_name))
        
        
        selected_track_index = self.selected_track_index
        if (selected_track_index != -1):
            if field_added:
                repr_parts.append(',')
            else:
                field_added = True
            
            repr_parts.append(' selected_track_index=')
            repr_parts.append(repr(selected_track_index))
        
        
        tracks = self.tracks
        if (tracks is not None):
            if field_added:
                repr_parts.append(',')
            
            repr_parts.append(' tracks=[')
            
            index = 0
            length = len(tracks)
            
            while True:
                track = tracks[index]
                repr_parts.append(repr(track))
                
                index += 1
                if index == length:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    def __len__(self):
        """Returns the length of the tracks."""
        tracks = self.tracks
        if tracks is None:
            length = 0
        else:
            length = len(tracks)
        
        return length
    
    
    def __bool__(self):
        """Returns whether the result has any tracks."""
        tracks = self.tracks
        if tracks is None:
            has_tracks = True
        else:
            if tracks:
                has_tracks = True
            else:
                has_tracks = False
        
        return has_tracks
    
    
    def __getitem__(self, index):
        """Returns the track of the given index"""
        tracks = self.tracks
        if tracks is None:
            raise IndexError(index)
        
        return tracks[index]
    
    
    def __hash__(self):
        """Returns the get tracks result's hash."""
        hash_value = 0
        
        playlist_name = self.playlist_name
        if (playlist_name is not None):
            hash_value ^= hash(playlist_name)
        
        selected_track_index = self.selected_track_index
        if (selected_track_index != -1):
            hash_value ^= (selected_track_index + 1)
        
        tracks = self.tracks
        if (tracks is not None):
            hash_value ^= (len(tracks) << 8)
            
            for track in tracks:
                hash_value ^= hash(track)
        
        return hash_value
    
    
    def __eq__(self, other):
        """Returns whether the two results are the same."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.playlist_name != other.playlist_name:
            return False
        
        if self.selected_track_index != other.selected_track_index:
            return False
        
        if self.tracks != other.tracks:
            return False
        
        return True
