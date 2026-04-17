import vampytest

from ..fields import put_embed_providers


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
            'embed_provider': [],
        },
    )
    
    yield (
        (
            'fry',
            'shrimp',
        ),
        False,
        {
            'embed_provider': [
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
            'embed_provider': [
                'fry',
                'shrimp',
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_embed_providers(input_value, defaults):
    """
    Tests whether ``put_embed_providers`` is working as intended.
    
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
    return put_embed_providers(input_value, {}, defaults)
