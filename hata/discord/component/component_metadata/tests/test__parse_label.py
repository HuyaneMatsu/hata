import vampytest

from ..fields import parse_label


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'label': None,
        },
        None,
    )
    
    yield (
        {
            'label': '',
        },
        None,
    )
    
    yield (
        {
            'label': 'a',
        },
        'a',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_label(input_data):
    """
    Tests whether ``parse_label`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    output = parse_label(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output
