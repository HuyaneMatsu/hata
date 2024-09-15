__all__ = ()

from .constants import MAX_UINT_16, MAX_UINT_32, RTP_PACKET_TYPE_VOICE


def create_rtp_header_lite(sequence_number, timestamp, source):
    """
    Creates an rtp header data litely. Only the minimal fields.
    
    Parameters
    ----------
    sequence_number : `int`
        Sequence number.
    
    timestamp : `int`
        Timestamp.
    
    source : `int`
        Packet source.
    
    Returns
    -------
    data : `bytes`
    """
    return b''.join([
        b'\x80', # version = 2, nothing else
        RTP_PACKET_TYPE_VOICE.to_bytes(1, 'big'),
        (sequence_number & MAX_UINT_16).to_bytes(2, 'big'),
        (timestamp & MAX_UINT_32).to_bytes(4, 'big'),
        source.to_bytes(4, 'big'),
    ])


def create_rtp_data_lite(header, payload, padding):
    """
    Creates an rtp data litely.
    
    Parameters
    ----------
    header : `bytes`
        Header data.
    
    payload : `bytes-like`
        Payload
    
    padding : `None | bytes-like`
        Padding if any.
    
    Returns
    -------
    data : `bytes`
    """
    if (padding is None) or (not padding):
        return header + payload
    
    return b''.join([header, payload, padding])
