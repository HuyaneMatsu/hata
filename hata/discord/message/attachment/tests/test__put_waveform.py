import vampytest

from ..fields import put_waveform


def _iter_options():
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'waveform': None,
        }
    )
    
    yield (
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        False,
        {
            'waveform':'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==',
        },
    )
    
    yield (
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
        True,
        {
            'waveform':'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==',
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_waveform(input_value, defaults):
    """
    Tests whether ``put_waveform`` works as intended.
    
    Parameters
    ----------
    input_value : `None | bytes`
        The value to serialise.
    
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_waveform(input_value, {}, defaults)
