import vampytest

from ..fields import parse_embed_providers


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'embed_provider': None,
        },
        None,
    )
    
    yield (
        {
            'embed_provider': [],
        },
        None,
    )
    
    yield (
        {
            'embed_provider': [
                'fry',
                'shrimp',
            ],
        },
        (
            'fry',
            'shrimp',
        ),
    )
    
    yield (
        {
            'embed_provider': [
                'shrimp',
                'fry',
            ],
        },
        (
            'fry',
            'shrimp',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_embed_providers(input_data):
    """
    Tests whether ``parse_embed_providers`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<str>`
    """
    output = parse_embed_providers(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, str)
    
    return output
