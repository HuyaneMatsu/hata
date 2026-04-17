import vampytest

from ..shared_fields import parse_label


def _iter_options():
    yield (
        {},
        '',
    )
    
    yield (
        {
            'label': '',
        },
        '',
    )
    
    yield (
        {
            'label': '',
        },
        '',
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
    output : `str`
    """
    output = parse_label(input_data)
    vampytest.assert_instance(output, str)
    return output
