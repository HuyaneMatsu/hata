import vampytest

from ..utils import create_rtp_data_lite


def test__create_rtp_data_lite__no_padding():
    """
    Tests whether ``create_rtp_data_lite`` works as intended.
    
    Case: without padding.
    """
    header = b'\x80x\x00\x14\x00\x00\x00y\x00\x00\x04\xb0'
    data = b'miau'
    
    output = create_rtp_data_lite(header, data, None)
    vampytest.assert_instance(output, bytes)
    vampytest.assert_eq(output, b''.join([header, data]))
    
    
def test__create_rtp_data_lite__with_padding():
    """
    Tests whether ``create_rtp_data_lite`` works as intended.
    
    Case: with padding.
    """
    header = b'\x80x\x00\x14\x00\x00\x00y\x00\x00\x04\xb0'
    data = b'miau'
    padding = b'\x00\x00\x00\x04'
    
    output = create_rtp_data_lite(header, data, padding)
    vampytest.assert_instance(output, bytes)
    vampytest.assert_eq(output, b''.join([header, data, padding]))
