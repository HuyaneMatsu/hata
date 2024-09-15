import vampytest

from ....client import Client

from ...packets.rtp_packet import RTPPacket
from ...packets.utils import create_rtp_header_lite, create_rtp_data_lite
from ...voice_client import VoiceClient

from ..aead_aes256_gcm_rtpsize import EncryptionAdapter__aead_aes256_gcm_rtpsize


def _assert_fields_set(encryption_adapter):
    """
    Asserts whether the given encryption adapter has all of its fields set.
    
    Parameters
    ----------
    encryption_adapter : ``EncryptionAdapter__aead_aes256_gcm_rtpsize``
        Encryption adapter to test.
    """
    vampytest.assert_instance(encryption_adapter, EncryptionAdapter__aead_aes256_gcm_rtpsize)
    vampytest.assert_instance(encryption_adapter.key, bytes)
    vampytest.assert_instance(encryption_adapter.nonce_counter, int)
    
    vampytest.assert_instance(encryption_adapter.available, bool)
    vampytest.assert_instance(encryption_adapter.key_length, int)
    vampytest.assert_instance(encryption_adapter.name, str)
    vampytest.assert_instance(encryption_adapter.nonce_length, int)
    vampytest.assert_instance(encryption_adapter.priority, int)


def test__EncryptionAdapter__aead_aes256_gcm_rtpsize__new():
    """
    Tests whether ``EncryptionAdapter__aead_aes256_gcm_rtpsize.__new__`` works as intended.
    """
    key = b'a' * EncryptionAdapter__aead_aes256_gcm_rtpsize.key_length
    
    encryption_adapter = EncryptionAdapter__aead_aes256_gcm_rtpsize(key)
    _assert_fields_set(encryption_adapter)
    
    vampytest.assert_eq(encryption_adapter.key, key)


def test__EncryptionAdapter__aead_aes256_gcm_rtpsize__repr():
    """
    Tests whether ``EncryptionAdapter__aead_aes256_gcm_rtpsize.__repr__`` works as intended.
    """
    key = b'a' * EncryptionAdapter__aead_aes256_gcm_rtpsize.key_length
    
    encryption_adapter = EncryptionAdapter__aead_aes256_gcm_rtpsize(key)
    output = repr(encryption_adapter)
    
    vampytest.assert_instance(output, str)


def test__EncryptionAdapter__aead_aes256_gcm_rtpsize__create_send_packet():
    """
    Tests whether ``EncryptionAdapter__aead_aes256_gcm_rtpsize.create_send_packet`` works as intended.
    """
    client_id = 202409090003
    guild_id = 202409090004
    channel_id = 202409090005
    sequence = 20
    source = 1200
    timestamp = 42
    key = b'a' * EncryptionAdapter__aead_aes256_gcm_rtpsize.key_length
    nonce_counter = 4
    data = b'a' * 64
    payload = b"t^K\x98`[\x06\x88\x86\xe3i\xc21\xd2^\xf1\r\xf2\xc7\xc1\xe4\xd2\xa2+\xd6\xdf\xd8\x96\xfb\xf1j\xdbN\x82c\xe5(Z\x86 \x0c\x8f>\xfb\xe0'O\n\xeaq1g\x93\x08W\xc5\xe9\x81q\xff+!k\xc6\xef\x86v\x19\x927\x17-g\xda,\x94\xab\x7f\xef)"
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
        
        encryption_adapter = EncryptionAdapter__aead_aes256_gcm_rtpsize(key)
        encryption_adapter.nonce_counter = nonce_counter - 1
        
        output = encryption_adapter.create_send_packet(voice_client, data)
        
        vampytest.assert_instance(output, bytes)
        vampytest.assert_eq(output, packet)
        
    finally:
        client._delete()
        client = None


def test__EncryptionAdapter__aead_aes256_gcm_rtpsize__process_received_payload():
    """
    Tests whether ``EncryptionAdapter__aead_aes256_gcm_rtpsize.process_received_payload`` works as intended.
    """
    sequence = 20
    source = 1200
    timestamp = 42
    key = b'a' * EncryptionAdapter__aead_aes256_gcm_rtpsize.key_length
    nonce_counter = 4
    payload = b"t^K\x98`[\x06\x88\x86\xe3i\xc21\xd2^\xf1\r\xf2\xc7\xc1\xe4\xd2\xa2+\xd6\xdf\xd8\x96\xfb\xf1j\xdbN\x82c\xe5(Z\x86 \x0c\x8f>\xfb\xe0'O\n\xeaq1g\x93\x08W\xc5\xe9\x81q\xff+!k\xc6\xef\x86v\x19\x927\x17-g\xda,\x94\xab\x7f\xef)"
    packet = create_rtp_data_lite(
        create_rtp_header_lite(sequence, timestamp, source), payload, nonce_counter.to_bytes(4, 'big')
    )
    data = b'a' * 64
    
    encryption_adapter = EncryptionAdapter__aead_aes256_gcm_rtpsize(key)
    
    output = encryption_adapter.process_received_payload(RTPPacket(packet))
    
    vampytest.assert_instance(output, bytes)
    vampytest.assert_eq(output, data)
