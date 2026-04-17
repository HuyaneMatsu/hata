import vampytest

from ..fields import put_url_host_names


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
            'link_hostname': [],
        },
    )
    
    yield (
        (
            'fry',
            'shrimp',
        ),
        False,
        {
            'link_hostname': [
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
            'link_hostname': [
                'fry',
                'shrimp',
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_url_host_names(input_value, defaults):
    """
    Tests whether ``put_url_host_names`` is working as intended.
    
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
    return put_url_host_names(input_value, {}, defaults)
