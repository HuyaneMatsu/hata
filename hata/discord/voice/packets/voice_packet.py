__all__ = ()

from scarletio import RichAttributeErrorBaseType

from ..opus import OpusDecoder, opus

if opus is None:
    DECODER = None
else:
    DECODER = OpusDecoder()


class VoicePacket(RichAttributeErrorBaseType):
    """
    Represents a voice packet.
    
    Attributes
    ----------
    _cache_decoded : `None | bytes`
        Cache field for ``.decoded``.
    encoded : `bytes`
        Encoded yet to decrypt data.
    """
    __slots__ = ('_cache_decoded', 'encoded')
    
    def __new__(cls, encoded):
        """
        Creates a new voice packet.
        
        Parameters
        ----------
        encoded : `bytes`
            Not yet decoded voice data.
        """
        self = object.__new__(cls)
        self.encoded = encoded
        self._cache_decoded = None
        return self
    
    
    def __repr__(self):
        """Returns the voice packet's representation."""
        repr_parts = ['<', type(self).__name__, '>']
        return ''.join(repr_parts)
    
    
    def __eq__(self, other):
        """Returns whether the two packets are equal."""
        if type(self) is not type(other):
            return False
        
        return self.encoded == other.encoded
    
    
    def __hash__(self):
        """Returns the voice packet's hash value."""
        return hash(self.encoded)
    
    
    @property
    def decoded(self):
        """
        Returns the voice packet's decoded data.
        
        Returns
        -------
        data : `bytes`
        """
        decoded = self._cache_decoded
        if decoded is None:
            assert DECODER is not None
            decoded = DECODER.decode(self.encoded)
            self._cache_decoded = decoded
        
        return decoded
