import vampytest

from ....client import Client

from ...packets.rtp_packet import RTPPacket
from ...packets.utils import create_rtp_header_lite, create_rtp_data_lite
from ...voice_client import VoiceClient

from ..base import EncryptionAdapterBase


def _assert_fields_set(encryption_adapter):
    """
    Asserts whether the given encryption adapter has all of its fields set.
    
    Parameters
    ----------
    encryption_adapter : ``EncryptionAdapterBase``
        Encryption adapter to test.
    """
    vampytest.assert_instance(encryption_adapter, EncryptionAdapterBase)
    vampytest.assert_instance(encryption_adapter.key, bytes)
    
    vampytest.assert_instance(encryption_adapter.available, bool)
    vampytest.assert_instance(encryption_adapter.key_length, int)
    vampytest.assert_instance(encryption_adapter.name, str)
    vampytest.assert_instance(encryption_adapter.nonce_length, int)
    vampytest.assert_instance(encryption_adapter.priority, int)


def test__EncryptionAdapterBase__new():
    """
    Tests whether ``EncryptionAdapterBase.__new__`` works as intended.
    """
    key = b'a' * EncryptionAdapterBase.key_length
    
    encryption_adapter = EncryptionAdapterBase(key)
    _assert_fields_set(encryption_adapter)
    
    vampytest.assert_eq(encryption_adapter.key, key)


def test__EncryptionAdapterBase__repr():
    """
    Tests whether ``EncryptionAdapterBase.__repr__`` works as intended.
    """
    key = b'a' * EncryptionAdapterBase.key_length
    
    encryption_adapter = EncryptionAdapterBase(key)
    output = repr(encryption_adapter)
    
    vampytest.assert_instance(output, str)


def test__EncryptionAdapterBase__create_send_packet():
    """
    Tests whether ``EncryptionAdapterBase.create_send_packet`` works as intended.
    """
    client_id = 202409090000
    guild_id = 202409090001
    channel_id = 202409090002
    sequence = 20
    source = 1200
    timestamp = 42
    key = b'a' * EncryptionAdapterBase.key_length
    data = b'a' * 64
    packet = b''
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        voice_client = VoiceClient(client, guild_id, channel_id)
        voice_client._sequence = sequence
        voice_client._audio_source = source
        voice_client._timestamp = timestamp
        
        encryption_adapter = EncryptionAdapterBase(key)
        
        output = encryption_adapter.create_send_packet(voice_client, data)
        
        vampytest.assert_instance(output, bytes)
        vampytest.assert_eq(output, packet)
        
    finally:
        client._delete()
        client = None


def test__EncryptionAdapterBase__process_received_payload():
    """
    Tests whether ``EncryptionAdapterBase.process_received_payload`` works as intended.
    """
    sequence = 20
    source = 1200
    timestamp = 42
    key = b'a' * EncryptionAdapterBase.key_length
    payload = b'a' * 64
    packet = create_rtp_data_lite(create_rtp_header_lite(sequence, timestamp, source), payload, None)
    data = b''
    
    encryption_adapter = EncryptionAdapterBase(key)
    
    output = encryption_adapter.process_received_payload(RTPPacket(packet))
    
    vampytest.assert_instance(output, bytes)
    vampytest.assert_eq(output, data)

