__all__ = ()

from scarletio import RichAttributeErrorBaseType


class EncryptionAdapterBase(RichAttributeErrorBaseType):
    """
    Base encryption adapter.
    
    Attributes
    ----------
    key : `bytes`
        Secret key used for encrypting / decrypting.
    """
    __slots__ = ('key', )
    
    available = False
    key_length = 0
    name = ''
    nonce_length = 0
    priority = 0
    
    
    def __new__(cls, key):
        """
        Instantiates a new encryption adapter.
        
        Parameters
        ----------
        key : `bytes`
            Key to use.
        """
        self = object.__new__(cls)
        self.key = key
        return self
    
    
    def __repr__(self):
        """Returns the encryption adapter's representation."""
        repr_parts = ['<', type(self).__name__]
        
        repr_parts.append(' key = ')
        repr_parts.append(repr(self.key))
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def create_send_packet(self, voice_client, plain_data):
        """
        Creates a send packet.
        
        Parameters
        ----------
        voice_client : ``VoiceClient``
            Voice client to send packet with.
        
        pain_data : `bytes-like`
            Data to encrypt.
        
        Returns
        -------
        packet : `bytes`
        """
        return b''
    
    
    def process_received_payload(self, rtp_packet):
        """
        Creates a send packet.
        
        Parameters
        ----------
        voice_client : ``VoiceClient``
            Voice client to send packet with.
        
        rtp_packet : `RTPPacket`
            Data to decrypt.
        
        Returns
        -------
        packet : `bytes`
        """
        return b''
