__all__ = ()

from scarletio import RichAttributeErrorBaseType

from .array import ArrayUInt32BE
from .constants import MAX_UINT_16, MAX_UINT_32


# used: 
# http://www.rfcreader.com/#rfc3550_line548
#
# not used:
# http://www.rfcreader.com/#rfc3550_line855
# http://www.rfcreader.com/#rfc3550_line1614
# #http://www.rfcreader.com/#rfc3550_line1879

# http://www.rfcreader.com/#rfc3550_line548

#    0                   1                   2                   3
#    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
#   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#   |V=2|P|E|  CC   |M|     PT      |       sequence number         |
#   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#   |                           timestamp                           |
#   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#   |                             source                            |
#   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# For each `CC` (contributing source count) :
#   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#   |               contributing source identifiers                 |
#   |                             ....                              |
#   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# If `E` (extended)
#   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#   |       extension profile       |      extension count          |
#   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# For each `extension count`
#   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#   |                       header extensions                       |
#   |                             ....                              |
#   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
#   +=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
#   |                           payload                             |
#   +=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
#
# For each `padding count - 1`, because it also includes the padding count field:
#   +-+-+-+-+-+-+-+-+
#   |    padding    |
#   +-+-+-+-+-+-+-+-+
#
# If `P` (padded)
#   +-+-+-+-+-+-+-+-+
#   | padding count |
#   +-+-+-+-+-+-+-+-+

def _iter_contributing_source_bytes(contributing_sources):
    """
    Iterates over and converts the given contributing sources to bytes.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    contributing_sources : `None | sequence<int>`
        Contributing sources.
    
    Yields
    ------
    source_bytes : `bytes`
    """
    if (contributing_sources is not None):
        for contributing_source in contributing_sources:
            yield contributing_source.to_bytes(4, 'big')


def _iter_extension_bytes(extension_profile, extensions):
    """
    Iterates over and converts the given extension information to bytes.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    extension_profile : `int`
        Extension profile.
    extensions : `None | sequence<int>`
        Extensions.
    
    Yields
    ------
    extension_bytes : `bytes`
    """
    if extension_profile or (extensions is not None):
        yield extension_profile.to_bytes(2, 'big')
        yield (0 if extensions is None else len(extensions)).to_bytes(2, 'big')
        
        if (extensions is not None):
            for extension in extensions:
                yield extension.to_bytes(4, 'big')


def _iter_padding_bytes(padding):
    """
    Yields back the padding. 
    
    This function is an iterable generator.
    
    Parameters
    ----------
    padding : `None | bytes-like`
        Padding if any.
    
    Yields
    ------
    padding_bytes : `bytes-like`
    """
    if (padding is not None):
        yield padding


class RTPPacket(RichAttributeErrorBaseType):
    """
    Represents an RTP packet.
    
    Attributes
    ----------
    data : `bytes`
        The raw data of the packet on what it is casted on.
    """
    __slots__ = ('data',)
    
    def __new__(cls, data):
        """
        Creates a new rtp packet with the given data.
        
        Parameters
        ----------
        data : `bytes`
        """
        self = object.__new__(cls)
        self.data = data
        return self
    
    
    @property
    def version(self):
        """
        Returns the rtp packet's version.
        
        Returns
        -------
        version : `int`
        """
        return self.data[0] >> 6
    
    
    @property
    def padded(self):
        """
        Returns whether the rtp packet is padded.
        
        Returns
        -------
        padded : `bool`
        """
        return True if (self.data[0] & 0b00100000) else False
    
    
    @property
    def extended(self):
        """
        Returns whether the rtp packet is extended.
        
        Returns
        -------
        extended : `bool`
        """
        return True if (self.data[0] & 0b00010000) else False
    
    
    @property
    def contributing_source_count(self):
        """
        Returns the contributing source count.
        
        Returns
        -------
        contributing_source_count : `int`
        """
        return self.data[0] & 0b00001111
    
    
    @property
    def marker(self):
        """
        Returns whether the packet is a marker.
        
        Returns
        -------
        marker : `bool`
        """
        return True if (self.data[1] & 0b10000000) else False
    
    
    @property
    def payload_type(self):
        """
        Returns the payload's type.
        
        Returns
        -------
        payload_type : `int`
        """
        return self.data[1] & 0b01111111
    
    
    @property
    def sequence(self):
        """
        Returns the sequence number.
        
        Returns
        -------
        sequence : `bool`
        """
        return int.from_bytes(self.data[2 : 4], 'big')
    
    
    @property
    def timestamp(self):
        """
        Returns the timestamp.
        
        Returns
        -------
        timestamp : `bool`
        """
        return int.from_bytes(self.data[4 : 8], 'big')
    
    
    @property
    def source(self):
        """
        Returns the source number.
        
        Returns
        -------
        source : `int`
        """
        return int.from_bytes(self.data[8 : 12], 'big')
    
    
    @property
    def header(self):
        """
        Returns the base of the header.
        
        Returns
        -------
        header : `bytes | memoryview`
        """
        data = self.data
        if len(data) <= 12:
            return data
        
        return memoryview(self.data)[ : 12]
    
    
    @property
    def contributing_sources(self):
        """
        Returns the contributing sources.
        
        Returns
        -------
        contributing_sources : `None | ArrayUInt32BE`
        """
        if not self.contributing_source_count:
            return None
        
        return ArrayUInt32BE(self.data, 12, self.extension_header_start)
    
    
    @property
    def extension_header_start(self):
        """
        Returns where the extension headers start.
        
        Returns
        -------
        extension_header_start : `int`
        """
        return 12 + (self.contributing_source_count << 2)
    
    
    @property
    def extension_profile(self):
        """
        Returns the extension profile.
        
        Returns
        -------
        extension_profile : `int`
        """
        if not self.extended:
            return 0
        
        start = self.extension_header_start
        return int.from_bytes(self.data[start : start + 2], 'big')
    
    
    @property
    def extension_count(self):
        """
        Returns the amount of extensions.
        
        Returns
        -------
        extension_count : `int`
        """
        if not self.extended:
            return 0
        
        start = self.extension_header_start + 2
        length = int.from_bytes(self.data[start : start + 2], 'big')
        return length
    
    
    @property
    def extensions(self):
        """
        Returns the extension values.
        
        Returns
        -------
        extensions : `None | ArrayUInt32BE`
        """
        extension_count = self.extension_count
        if not extension_count:
            return None
        
        
        start = self.extension_header_start + 4
        end = start + (extension_count << 2)
        
        return ArrayUInt32BE(self.data, start, end)
    
    
    @property
    def payload_start(self):
        """
        Returns where the payload starts.
        
        Returns
        -------
        payload_start : `int`
        """
        start = self.extension_header_start
        extension_count = self.extension_count
        if extension_count:
            start += 4 + (extension_count << 2)
        
        return start
    
    
    @property
    def payload_end(self):
        """
        Returns where the payload ends.
        
        Returns
        -------
        payload_end : `int`
        """
        return len(self.data) - self.padding_count
    
    
    @property
    def payload(self):
        """
        Returns the payload.
        
        Returns
        -------
        payload : `memoryview`
        """
        return memoryview(self.data)[self.payload_start : self.payload_end]
    
    
    @property
    def padding_count(self):
        """
        Returns the amount of paddings.
        
        Returns
        -------
        padding_count : `int`
        """
        padded = self.padded
        if not padded:
            return 0
        
        return self.data[-1]
    
    
    @property
    def padding(self):
        """
        Returns the padding.
        
        Returns
        -------
        padding : `None | memoryview`
        """
        padding_count = self.padding_count
        if not padding_count:
            return None
        
        return memoryview(self.data)[-padding_count : ]
    
    
    @classmethod
    def from_fields(
        cls,
        version,
        padding,
        extension_profile,
        extensions,
        contributing_sources,
        marker,
        payload_type,
        sequence_number,
        timestamp,
        source,
        payload,
    ):
        """
        Creates a new rtp packet from the given fields.
        
        Parameters
        ----------
        version : `int`
            Version number.
        
        padding : `None | bytes-like`
            Padding if any.
        
        extension_profile : `int`
            Extension profile.
        
        extensions : `None | sequence<int>`
            Extensions.
        
        contributing_sources : `None | sequence<int>`
            Contributing sources.
        
        marker : `bool`
            Whether the packet is a marker.
        
        payload_type : `int`
            The payload's type.
        
        sequence_number : `int`
            Sequence number.
        
        timestamp : `int`
            Timestamp.
        
        source : `int`
            Packet source.
        
        payload : `bytes-like`
            The payload itself.
        
        Returns
        -------
        self : `instance<cls>`
        
        Raises
        ------
        TypeError
            - If a parameter's type is invalid.
        ValueError
            - If a parameter's value is invalid.
        """
        if extension_profile or (extensions is not None):
            extended = True
        else:
            extended = False
        
        if (padding is not None) or (not padding):
            padded = True
            if padding[-1] != len(padding):
                raise ValueError(f'Last byte of batting must be equal to its length; got padding = {padding!r}')
        
        else:
            padded = False
        
        if contributing_sources is None:
            contributing_source_count = 0
        else:
            contributing_source_count = len(contributing_sources)
        
        
        data = b''.join([
            ((version << 6) | ((padded << 5)) | (extended << 4) | contributing_source_count).to_bytes(1, 'big'),
            ((marker << 7) | payload_type).to_bytes(1, 'big'),
            (sequence_number & MAX_UINT_16).to_bytes(2, 'big'),
            (timestamp & MAX_UINT_32).to_bytes(4, 'big'),
            source.to_bytes(4, 'big'),
            *_iter_contributing_source_bytes(contributing_sources),
            *_iter_extension_bytes(extension_profile, extensions),
            payload,
            *_iter_padding_bytes(padding),
        ])
        
        self = object.__new__(cls)
        self.data = data
        return self
    
    
    def __repr__(self):
        """Returns the packet's representation."""
        repr_parts = ['<', type(self).__name__]
        
        # version
        repr_parts.append(' version = ')
        repr_parts.append(repr(self.version))
        
        # padded (padding)
        padding = self.padding
        if (padding is not None):
            repr_parts.append(', padding = ')
            repr_parts.append(repr(padding))
        
        # extended (extension_profile, extension)
        extension_profile = self.extension_profile
        extensions = self.extensions
        if extension_profile or (extensions is not None):
            repr_parts.append(', extension_profile = ')
            repr_parts.append(repr(extension_profile))
            
            repr_parts.append(', extensions = ')
            repr_parts.append(repr(extensions))
        
        # contributing_sources
        contributing_sources = self.contributing_sources
        if (contributing_sources is not None):
            repr_parts.append(', contributing_sources = ')
            repr_parts.append(repr(contributing_sources))
        
        # marker
        marker = self.marker
        if marker:
            repr_parts.append(', marker = ')
            repr_parts.append(repr(marker))
        
        # payload_type
        repr_parts.append(', payload_type = ')
        repr_parts.append(repr(self.payload_type))
        
        # sequence
        repr_parts.append(', sequence = ')
        repr_parts.append(repr(self.sequence))
        
        # timestamp
        repr_parts.append(', timestamp = ')
        repr_parts.append(repr(self.timestamp))
        
        # source
        repr_parts.append(', source = ')
        repr_parts.append(repr(self.source))
        
        # payload
        payload = self.payload
        if payload:
            repr_parts.append(', payload (length) = ')
            repr_parts.append(repr(len(payload)))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two rtp packets are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        return self.data == other.data
    
    
    def __hash__(self):
        """Returns the rtp packet's hash value."""
        return hash(self.data)
