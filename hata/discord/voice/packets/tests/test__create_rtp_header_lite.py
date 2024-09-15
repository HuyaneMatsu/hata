import vampytest

from ..utils import create_rtp_header_lite


def test__create_rtp_header_lite():
    """
    Tests whether ``create_rtp_header_lite`` works as intended.
    """
    sequence_number = 20
    timestamp = 121
    source = 1200
    
    output = create_rtp_header_lite(sequence_number, timestamp, source)
    vampytest.assert_instance(output, bytes)
    
    vampytest.assert_eq(
        output,
        (
            b'\x80x'
            b'\x00\x14'
            b'\x00\x00\x00y'
            b'\x00\x00\x04\xb0'
        ),
    )
