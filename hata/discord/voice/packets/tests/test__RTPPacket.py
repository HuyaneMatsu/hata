import vampytest

from ..rtp_packet import RTPPacket

TEST_VERSION = 2
TEST_PADDED = True
TEST_EXTENDED = True
TEST_CONTRIBUTING_SOURCE_COUNT = 3
TEST_MARKER = True
TEST_PAYLOAD_TYPE = 4
TEST_SEQUENCE_NUMBER = 12
TEST_TIMESTAMP = 4566
TEST_SOURCE = 12000
TEST_CONTRIBUTING_SOURCES = [1333, 1444, 1555]
TEST_EXTENSION_PROFILE = 456
TEST_EXTENSION_COUNT = 3
TEST_EXTENSIONS = [133, 144, 2]
TEST_PAYLOAD = b'miauland'
TEST_PADDING_COUNT = 4
TEST_PADDING = b'\x00\x00\x00\x04'
TEST_EXTENSION_HEADER_START = 12 + (TEST_CONTRIBUTING_SOURCE_COUNT << 2)
TEST_PAYLOAD_START = TEST_EXTENSION_HEADER_START + 4 + (TEST_EXTENSION_COUNT << 2)
TEST_PAYLOAD_END = TEST_PAYLOAD_START + len(TEST_PAYLOAD)


TEST_DATA = b''.join([
    (
        (TEST_VERSION << 6) |
        (TEST_PADDED << 5) |
        (TEST_EXTENDED << 4) |
        TEST_CONTRIBUTING_SOURCE_COUNT
    ).to_bytes(1, 'big'),
    (
        (TEST_MARKER << 7) |
        TEST_PAYLOAD_TYPE
    ).to_bytes(1, 'big'),
    TEST_SEQUENCE_NUMBER.to_bytes(2, 'big'),
    TEST_TIMESTAMP.to_bytes(4, 'big'),
    TEST_SOURCE.to_bytes(4, 'big'),
    *(value.to_bytes(4, 'big') for value in TEST_CONTRIBUTING_SOURCES),
    TEST_EXTENSION_PROFILE.to_bytes(2, 'big'),
    TEST_EXTENSION_COUNT.to_bytes(2, 'big'),
    *(value.to_bytes(4, 'big') for value in TEST_EXTENSIONS),
    TEST_PAYLOAD,
    TEST_PADDING,
])


def _assert_fields_set(rtp_packet):
    """
    Asserts whether every fields are set of the rtp packet.
    
    Parameters
    ----------
    rtp_packet : ``RTPPacket``
        The packet to test.
    """
    vampytest.assert_instance(rtp_packet, RTPPacket)
    vampytest.assert_instance(rtp_packet.data, bytes)


def test__RTPPacket__new():
    """
    Tests whether ``RTPPacket.__new__`` works as intended.
    """
    rtp_packet = RTPPacket(TEST_DATA)
    _assert_fields_set(rtp_packet)
    vampytest.assert_eq(rtp_packet.data, TEST_DATA)
    
    vampytest.assert_eq(rtp_packet.version, TEST_VERSION)
    vampytest.assert_eq(rtp_packet.padded, TEST_PADDED)
    vampytest.assert_eq(rtp_packet.extended, TEST_EXTENDED)
    vampytest.assert_eq(rtp_packet.contributing_source_count, TEST_CONTRIBUTING_SOURCE_COUNT)
    vampytest.assert_eq(rtp_packet.marker, TEST_MARKER)
    vampytest.assert_eq(rtp_packet.payload_type, TEST_PAYLOAD_TYPE)
    vampytest.assert_eq(rtp_packet.sequence, TEST_SEQUENCE_NUMBER)
    vampytest.assert_eq(rtp_packet.timestamp, TEST_TIMESTAMP)
    vampytest.assert_eq(rtp_packet.source, TEST_SOURCE)
    vampytest.assert_eq([*rtp_packet.contributing_sources], TEST_CONTRIBUTING_SOURCES)
    vampytest.assert_eq(rtp_packet.extension_profile, TEST_EXTENSION_PROFILE)
    vampytest.assert_eq(rtp_packet.extension_count, TEST_EXTENSION_COUNT)
    vampytest.assert_eq([*rtp_packet.extensions], TEST_EXTENSIONS)
    vampytest.assert_eq(rtp_packet.payload, TEST_PAYLOAD)
    vampytest.assert_eq(rtp_packet.padding_count, TEST_PADDING_COUNT)
    vampytest.assert_eq(rtp_packet.padding, TEST_PADDING)
    vampytest.assert_eq(rtp_packet.extension_header_start, TEST_EXTENSION_HEADER_START)
    vampytest.assert_eq(rtp_packet.payload_start, TEST_PAYLOAD_START)
    vampytest.assert_eq(rtp_packet.payload_end, TEST_PAYLOAD_END)
    vampytest.assert_eq(rtp_packet.header, TEST_DATA[:12])


def test__RTPPacket__from_fields():
    """
    Tests whether ``RTPPacket.from_fields`` works as intended.
    """
    rtp_packet = RTPPacket.from_fields(
        TEST_VERSION,
        TEST_PADDING,
        TEST_EXTENSION_PROFILE,
        TEST_EXTENSIONS,
        TEST_CONTRIBUTING_SOURCES,
        TEST_MARKER,
        TEST_PAYLOAD_TYPE,
        TEST_SEQUENCE_NUMBER,
        TEST_TIMESTAMP,
        TEST_SOURCE,
        TEST_PAYLOAD,
    )
    _assert_fields_set(rtp_packet)
    vampytest.assert_eq(rtp_packet.data, TEST_DATA)


def test__RTPPacket__repr():
    """
    Tests whether ``RTPPacket.__repr__`` works as intended.
    """
    rtp_packet = RTPPacket(TEST_DATA)
    
    output = repr(rtp_packet)
    vampytest.assert_instance(output, str)


def test__RTPPacket__eq():
    """
    Tests whether ``RTPPacket.__eq__`` works as intended.
    """
    rtp_packet_0 = RTPPacket(TEST_DATA)
    rtp_packet_1 = RTPPacket(b'\x00' * 12)
    
    vampytest.assert_eq(rtp_packet_0, rtp_packet_0)
    vampytest.assert_ne(rtp_packet_0, rtp_packet_1)
    vampytest.assert_eq(rtp_packet_1, rtp_packet_1)


def test__RTPPacket__hash():
    """
    Tests whether ``RTPPacket.__hash__`` works as intended.
    """
    rtp_packet = RTPPacket(TEST_DATA)
    
    output = hash(rtp_packet)
    vampytest.assert_instance(output, int)
