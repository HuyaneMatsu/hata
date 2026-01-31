import vampytest

from ..fields import put_aliases


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
            'aliases': [],
        },
    )
    
    yield (
        (
            'fry',
            'shrimp',
        ),
        False,
        {
            'aliases': [
                'fry',
                'shrimp',
            ],
        },
    )
    
    yield (
        (
            'fry',
            'shrimp',
        ),
        True,
        {
            'aliases': [
                'fry',
                'shrimp',
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_aliases(input_value, defaults):
    """
    Tests whether ``put_aliases`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<str>`
        The value to serialise.
    
    defaults : `bool`
        Whether fields as their defaults should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_aliases(input_value, {}, defaults)
