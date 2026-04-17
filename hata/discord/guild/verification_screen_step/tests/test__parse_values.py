import vampytest

from ..fields import parse_values


def _iter_options():
    yield (
        {},
        None,
    )
    
    
    yield (
        {
            'values': None,
        },
        None,
    )
    
    yield (
        {
            'values': [],
        },
        None,
    )
    
    yield (
        {
            'values': [
                'apple',
                'pear',
            ],
        },
        (
            'apple',
            'pear',
        ),
    )
    
    yield (
        {
            'values': [
                'pear',
                'apple',
            ],
        },
        (
            'apple',
            'pear',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_values(input_data):
    """
    Tests whether ``parse_values`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<str>`
    """
    output = parse_values(input_data)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, str)
    
    return output
