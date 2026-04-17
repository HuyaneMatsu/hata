import vampytest

from ..fields import parse_application_command_name


def _iter_options():
    yield (
        {},
        '',
    )
    
    yield (
        {
            'data': {
                'name': None,
            },
        },
        '',
    )
    
    yield (
        {
            'data': {
                'name': '',
            },
        },
        '',
    )
    
    yield (
        {
            'data': {
                'name': 'a',
            },
        },
        'a',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_application_command_name(input_data):
    """
    Tests whether ``parse_application_command_name`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse the name from.
    
    Returns
    -------
    name : `str`
    """
    output = parse_application_command_name(input_data)
    vampytest.assert_instance(output, str)
    return output
