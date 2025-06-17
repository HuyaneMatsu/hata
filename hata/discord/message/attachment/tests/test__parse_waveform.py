import vampytest

from ..fields import parse_waveform


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'waveform': None,
        },
        None,
    )
    
    yield (
        {
            'waveform': '',
        },
        None,
    )
    
    yield (
        {
            'waveform': 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==',
        },
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_waveform(input_data):
    """
    Tests whether ``parse_waveform`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse the waveform from.
    
    Returns
    -------
    waveform : `None | bytes`
    """
    output = parse_waveform(input_data)
    vampytest.assert_instance(output, bytes, nullable = True)
    return output
