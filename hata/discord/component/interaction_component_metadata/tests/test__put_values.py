import vampytest

from ..fields import put_values


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
            'values': [],
        }
    )
    
    yield (
        (
            'apple',
            'pear',
        ),
        False,
        {
            'values': [
                'apple',
                'pear',
            ],
        },
    )
    
    yield (
        (
            'apple',
            'pear',
        ),
        True,
        {
            'values': [
                'apple',
                'pear',
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_values(input_value, defaults):
    """
    Tests whether ``put_values`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<str>`
        Value to serialize.
    
    defaults : `bool`
        whether fields as their defaults should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_values(input_value, {}, defaults)
