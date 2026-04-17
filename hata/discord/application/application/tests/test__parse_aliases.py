import vampytest

from ..fields import parse_aliases


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'aliases': None,
        },
        None,
    )
    
    yield (
        {
            'aliases': [],
        },
        None,
    )
    
    yield (
        {
            'aliases': [
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
            'aliases': [
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
def test__parse_aliases(input_data):
    """
    Tests whether ``parse_aliases`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<str>`
    """
    output = parse_aliases(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, str)
    
    return output
