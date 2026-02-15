import vampytest

from ..fields import put_value__bool


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
            'value': None,
        },
    )
    
    yield (
        '\00',
        False,
        {
            'value': False,
        },
    )
    
    yield (
        '\00',
        True,
        {
            'value': False,
        },
    )
    
    yield (
        '\01',
        False,
        {
            'value': True,
        },
    )
    
    yield (
        '\01',
        True,
        {
            'value': True,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_value__bool(input_value, defaults):
    """
    Tests whether ``put_value__bool`` works as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        Value to serialize.
    
    defaults : `bool`
        Whether values of their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_value__bool(input_value, {}, defaults)
