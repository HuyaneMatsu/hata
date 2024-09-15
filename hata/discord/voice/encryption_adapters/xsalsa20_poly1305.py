__all__ = ()

from scarletio import copy_docs

from ..packets.utils import create_rtp_data_lite, create_rtp_header_lite

from .base import EncryptionAdapterBase

try:
    from libnacl import crypto_secretbox, crypto_secretbox_KEYBYTES, crypto_secretbox_NONCEBYTES, crypto_secretbox_open
except ImportError:
    crypto_secretbox_KEYBYTES = 0
    crypto_secretbox_NONCEBYTES = 0
    crypto_secretbox = lambda plain_data, nonce, key: b''
    crypto_secretbox_open = lambda cipher_data, nonce, key: b''


class EncryptionAdapter__xsalsa20_poly1305(EncryptionAdapterBase):
    """
    `xsalsa20_poly1305` encryption adapter.
    
    Attributes
    ----------
    key : `bytes`
        Secret key used for encrypting / decrypting.
    """
    __slots__ = ()
    
    available = True if crypto_secretbox_KEYBYTES else False
    key_length = crypto_secretbox_KEYBYTES
    name = 'xsalsa20_poly1305'
    nonce_length = crypto_secretbox_NONCEBYTES
    priority = 1
    
    
    @copy_docs(EncryptionAdapterBase.__new__)
    def __new__(cls, key):
        self = object.__new__(cls)
        self.key = key
        return self
    
    
    @copy_docs(EncryptionAdapterBase.create_send_packet)
    def create_send_packet(self, voice_client, plain_data):
        header = create_rtp_header_lite(
            voice_client._sequence, voice_client._timestamp, voice_client._audio_source
        )
        nonce = header.ljust(self.nonce_length, b'\x00')
        payload = crypto_secretbox(plain_data, nonce, self.key)
        return create_rtp_data_lite(header, payload, None)
    
    
    @copy_docs(EncryptionAdapterBase.process_received_payload)
    def process_received_payload(self, rtp_packet):
        nonce = bytes(rtp_packet.header).ljust(self.nonce_length, b'\x00')
        return crypto_secretbox_open(bytes(rtp_packet.payload), nonce, self.key)
