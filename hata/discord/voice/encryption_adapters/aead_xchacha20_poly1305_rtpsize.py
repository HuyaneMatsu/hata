__all__ = ()

from random import randint

from scarletio import copy_docs

from ..packets.constants import MAX_UINT_32
from ..packets.utils import create_rtp_data_lite, create_rtp_header_lite

from .base import EncryptionAdapterBase

try:
    from libnacl import (
        crypto_aead_xchacha20poly1305_ietf_KEYBYTES, crypto_aead_xchacha20poly1305_ietf_NPUBBYTES,
        crypto_aead_xchacha20poly1305_ietf_decrypt, crypto_aead_xchacha20poly1305_ietf_encrypt
    )
except ImportError:
    crypto_aead_xchacha20poly1305_ietf_KEYBYTES = 0
    crypto_aead_xchacha20poly1305_ietf_NPUBBYTES = 0
    crypto_aead_xchacha20poly1305_ietf_encrypt = lambda cipher_data, additional_authentication_data, nonce, key: b''
    crypto_aead_xchacha20poly1305_ietf_decrypt = lambda plain_data, additional_authentication_data, nonce, key: b''


class EncryptionAdapter__aead_xchacha20_poly1305_rtpsize(EncryptionAdapterBase):
    """
    `aead_xchacha20_poly1305_rtpsize` encryption adapter.
    
    Attributes
    ----------
    key : `bytes`
        Secret key used for encrypting / decrypting.
    
    nonce_counter : `int`
        Incremental counter for generating nonces.
    """
    __slots__ = ('nonce_counter',)
    
    available = True if crypto_aead_xchacha20poly1305_ietf_KEYBYTES else False
    key_length = crypto_aead_xchacha20poly1305_ietf_KEYBYTES
    name = 'aead_xchacha20_poly1305_rtpsize'
    nonce_length = crypto_aead_xchacha20poly1305_ietf_NPUBBYTES
    priority = 3
    
    
    @copy_docs(EncryptionAdapterBase.__new__)
    def __new__(cls, key):
        self = object.__new__(cls)
        self.key = key
        self.nonce_counter = randint(0, MAX_UINT_32) % 487
        return self
    
    
    def get_next_nonce_bytes(self):
        """
        Increments the nonce counter and return a new nonce value generated from it.
        
        Returns
        -------
        nonce : `bytes`
        """
        nonce_counter = self.nonce_counter + 1
        self.nonce_counter = nonce_counter
        return (nonce_counter & MAX_UINT_32).to_bytes(4, 'big')
    
    
    @copy_docs(EncryptionAdapterBase.create_send_packet)
    def create_send_packet(self, voice_client, plain_data):
        header = create_rtp_header_lite(
            voice_client._sequence, voice_client._timestamp, voice_client._audio_source
        )
        nonce_bytes = self.get_next_nonce_bytes()
        nonce = nonce_bytes.ljust(self.nonce_length, b'\x00')
        payload = crypto_aead_xchacha20poly1305_ietf_encrypt(plain_data, header, nonce, self.key)
        return create_rtp_data_lite(header, payload, nonce_bytes)
    
    
    @copy_docs(EncryptionAdapterBase.process_received_payload)
    def process_received_payload(self, rtp_packet):
        # last 4 bits of payload is the nonce rest is the actual payload
        payload = rtp_packet.payload
        nonce = bytes(payload[-4 :]).ljust(self.nonce_length, b'\x00')
        payload = bytes(payload[: -4])
        
        return crypto_aead_xchacha20poly1305_ietf_decrypt(payload, bytes(rtp_packet.header), nonce, self.key)
