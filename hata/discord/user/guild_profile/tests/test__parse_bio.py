import vampytest

from ..fields import parse_bio


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'bio': None,
        },
        None,
    )
    
    yield (
        {
            'bio': '',
        },
        None,
    )
    
    yield (
        {
            'bio': 'a',
        },
        'a',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_bio(input_data):
    """
    Tests whether ``parse_bio`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    output = parse_bio(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output
