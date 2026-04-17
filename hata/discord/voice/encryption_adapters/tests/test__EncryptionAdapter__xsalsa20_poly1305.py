import vampytest

from ....client import Client

from ...packets.rtp_packet import RTPPacket
from ...packets.utils import create_rtp_header_lite, create_rtp_data_lite
from ...voice_client import VoiceClient

from ..xsalsa20_poly1305 import EncryptionAdapter__xsalsa20_poly1305


def _assert_fields_set(encryption_adapter):
    """
    Asserts whether the given encryption adapter has all of its fields set.
    
    Parameters
    ----------
    encryption_adapter : ``EncryptionAdapter__xsalsa20_poly1305``
        Encryption adapter to test.
    """
    vampytest.assert_instance(encryption_adapter, EncryptionAdapter__xsalsa20_poly1305)
    vampytest.assert_instance(encryption_adapter.key, bytes)
    
    vampytest.assert_instance(encryption_adapter.available, bool)
    vampytest.assert_instance(encryption_adapter.key_length, int)
    vampytest.assert_instance(encryption_adapter.name, str)
    vampytest.assert_instance(encryption_adapter.nonce_length, int)
    vampytest.assert_instance(encryption_adapter.priority, int)


def test__EncryptionAdapter__xsalsa20_poly1305__new():
    """
    Tests whether ``EncryptionAdapter__xsalsa20_poly1305.__new__`` works as intended.
    """
    key = b'a' * EncryptionAdapter__xsalsa20_poly1305.key_length
    
    encryption_adapter = EncryptionAdapter__xsalsa20_poly1305(key)
    _assert_fields_set(encryption_adapter)
    
    vampytest.assert_eq(encryption_adapter.key, key)


def test__EncryptionAdapter__xsalsa20_poly1305__repr():
    """
    Tests whether ``EncryptionAdapter__xsalsa20_poly1305.__repr__`` works as intended.
    """
    key = b'a' * EncryptionAdapter__xsalsa20_poly1305.key_length
    
    encryption_adapter = EncryptionAdapter__xsalsa20_poly1305(key)
    output = repr(encryption_adapter)
    
    vampytest.assert_instance(output, str)


def test__EncryptionAdapter__xsalsa20_poly1305__create_send_packet():
    """
    Tests whether ``EncryptionAdapter__xsalsa20_poly1305.create_send_packet`` works as intended.
    """
    client_id = 202409090006
    guild_id = 202409090007
    channel_id = 202409090008
    sequence = 20
    source = 1200
    timestamp = 42
    key = b'a' * EncryptionAdapter__xsalsa20_poly1305.key_length
    data = b'a' * 64
    payload = b'\xe4\n@\x0c:\xac\\$\xc9\x8a\x9c\xbcWv\xcf\n\xb4J\xca\xd7\xcd\xca\xcb\x82\xb5ns\xfcWr\xc3BnG\xd3\x87\xb1\x05JL1M\xf4\xf7\xc2O\xafSA\xe6\xa4\x14\xc7\xd0\xbb\xe9#0\xf9>\x17\xf7x\xf9\x07X\x92\xfc\x13\xc1\x9b\xe2\xde\xc6\x8e\xd3\xfcI\x8d\xf7'
    packet = create_rtp_data_lite(
        create_rtp_header_lite(sequence, timestamp, source), payload, None,
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
        
        encryption_adapter = EncryptionAdapter__xsalsa20_poly1305(key)
        
        output = encryption_adapter.create_send_packet(voice_client, data)
        
        vampytest.assert_instance(output, bytes)
        vampytest.assert_eq(output, packet)
        
    finally:
        client._delete()
        client = None


def test__EncryptionAdapter__xsalsa20_poly1305__process_received_payload():
    """
    Tests whether ``EncryptionAdapter__xsalsa20_poly1305.process_received_payload`` works as intended.
    """
    sequence = 20
    source = 1200
    timestamp = 42
    key = b'a' * EncryptionAdapter__xsalsa20_poly1305.key_length
    payload = b'\xe4\n@\x0c:\xac\\$\xc9\x8a\x9c\xbcWv\xcf\n\xb4J\xca\xd7\xcd\xca\xcb\x82\xb5ns\xfcWr\xc3BnG\xd3\x87\xb1\x05JL1M\xf4\xf7\xc2O\xafSA\xe6\xa4\x14\xc7\xd0\xbb\xe9#0\xf9>\x17\xf7x\xf9\x07X\x92\xfc\x13\xc1\x9b\xe2\xde\xc6\x8e\xd3\xfcI\x8d\xf7'
    packet = create_rtp_data_lite(
        create_rtp_header_lite(sequence, timestamp, source), payload, None,
    )
    data = b'a' * 64
    
    encryption_adapter = EncryptionAdapter__xsalsa20_poly1305(key)
    
    output = encryption_adapter.process_received_payload(RTPPacket(packet))
    
    vampytest.assert_instance(output, bytes)
    vampytest.assert_eq(output, data)
