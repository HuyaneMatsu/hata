import vampytest

from ....client import Client

from ...packets.rtp_packet import RTPPacket
from ...packets.utils import create_rtp_header_lite, create_rtp_data_lite
from ...voice_client import VoiceClient

from ..aead_xchacha20_poly1305_rtpsize import EncryptionAdapter__aead_xchacha20_poly1305_rtpsize


def _assert_fields_set(encryption_adapter):
    """
    Asserts whether the given encryption adapter has all of its fields set.
    
    Parameters
    ----------
    encryption_adapter : ``EncryptionAdapter__aead_xchacha20_poly1305_rtpsize``
        Encryption adapter to test.
    """
    vampytest.assert_instance(encryption_adapter, EncryptionAdapter__aead_xchacha20_poly1305_rtpsize)
    vampytest.assert_instance(encryption_adapter.key, bytes)
    vampytest.assert_instance(encryption_adapter.nonce_counter, int)
    
    vampytest.assert_instance(encryption_adapter.available, bool)
    vampytest.assert_instance(encryption_adapter.key_length, int)
    vampytest.assert_instance(encryption_adapter.name, str)
    vampytest.assert_instance(encryption_adapter.nonce_length, int)
    vampytest.assert_instance(encryption_adapter.priority, int)


def test__EncryptionAdapter__aead_xchacha20_poly1305_rtpsize__new():
    """
    Tests whether ``EncryptionAdapter__aead_xchacha20_poly1305_rtpsize.__new__`` works as intended.
    """
    key = b'a' * EncryptionAdapter__aead_xchacha20_poly1305_rtpsize.key_length
    
    encryption_adapter = EncryptionAdapter__aead_xchacha20_poly1305_rtpsize(key)
    _assert_fields_set(encryption_adapter)
    
    vampytest.assert_eq(encryption_adapter.key, key)


def test__EncryptionAdapter__aead_xchacha20_poly1305_rtpsize__repr():
    """
    Tests whether ``EncryptionAdapter__aead_xchacha20_poly1305_rtpsize.__repr__`` works as intended.
    """
    key = b'a' * EncryptionAdapter__aead_xchacha20_poly1305_rtpsize.key_length
    
    encryption_adapter = EncryptionAdapter__aead_xchacha20_poly1305_rtpsize(key)
    output = repr(encryption_adapter)
    
    vampytest.assert_instance(output, str)


def test__EncryptionAdapter__aead_xchacha20_poly1305_rtpsize__create_send_packet():
    """
    Tests whether ``EncryptionAdapter__aead_xchacha20_poly1305_rtpsize.create_send_packet`` works as intended.
    """
    client_id = 202409090006
    guild_id = 202409090007
    channel_id = 202409090008
    sequence = 20
    source = 1200
    timestamp = 42
    key = b'a' * EncryptionAdapter__aead_xchacha20_poly1305_rtpsize.key_length
    nonce_counter = 4
    data = b'a' * 64
    payload = b'\x07\xb3\xdb!\x065\x97\r#\x04T|v\xb5\xfa\xc0%"+o{\xc5\xa7+\xd08\x9a\xa1\xef\x11o\xd3\xc9\x03\xce\xf5-\x07\xa4\x97\xe9qbE\x06\x0c\x9f:p8\xa8\xc5\xb7^\x0b\x05\xc01\xafm\x9a\xe4\x07+U\x8e\xf3V\x176\x87\xe8r\x85\xff\xef\xc7YTW'
    packet = create_rtp_data_lite(
        create_rtp_header_lite(sequence, timestamp, source), payload, nonce_counter.to_bytes(4, 'big')
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        voice_client = VoiceClient(client, guild_id, channel_id)
        voice_client._sequence = sequence
        voice_client._audio_source = source
        voice_client._timestamp = timestamp
        
        encryption_adapter = EncryptionAdapter__aead_xchacha20_poly1305_rtpsize(key)
        encryption_adapter.nonce_counter = nonce_counter - 1
        
        output = encryption_adapter.create_send_packet(voice_client, data)
        
        vampytest.assert_instance(output, bytes)
        vampytest.assert_eq(output, packet)
        
    finally:
        client._delete()
        client = None


def test__EncryptionAdapter__aead_xchacha20_poly1305_rtpsize__process_received_payload():
    """
    Tests whether ``EncryptionAdapter__aead_xchacha20_poly1305_rtpsize.process_received_payload`` works as intended.
    """
    sequence = 20
    source = 1200
    timestamp = 42
    key = b'a' * EncryptionAdapter__aead_xchacha20_poly1305_rtpsize.key_length
    nonce_counter = 4
    payload = b'\x07\xb3\xdb!\x065\x97\r#\x04T|v\xb5\xfa\xc0%"+o{\xc5\xa7+\xd08\x9a\xa1\xef\x11o\xd3\xc9\x03\xce\xf5-\x07\xa4\x97\xe9qbE\x06\x0c\x9f:p8\xa8\xc5\xb7^\x0b\x05\xc01\xafm\x9a\xe4\x07+U\x8e\xf3V\x176\x87\xe8r\x85\xff\xef\xc7YTW'
    packet = create_rtp_data_lite(
        create_rtp_header_lite(sequence, timestamp, source), payload, nonce_counter.to_bytes(4, 'big')
    )
    data = b'a' * 64
    
    encryption_adapter = EncryptionAdapter__aead_xchacha20_poly1305_rtpsize(key)
    
    output = encryption_adapter.process_received_payload(RTPPacket(packet))
    
    vampytest.assert_instance(output, bytes)
    vampytest.assert_eq(output, data)
