import vampytest

from ..fields import put_application_command_name


def _iter_options():
    yield (
        '',
        False,
        {
            'data': {
                'name': '',
            },
        },
    )
    
    yield (
        '',
        True,
        {
            'data': {
                'name': '',
            },
        },
    )
    
    yield (
        'a',
        False,
        {
            'data': {
                'name': 'a',
            },
        },
    )
    
    yield (
        'a',
        True,
        {
            'data': {
                'name': 'a',
            },
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_application_command_name(input_value, defaults):
    """
    Tests whether ``put_application_command_name`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        The value to serialise.
    
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_application_command_name(input_value, {}, defaults)
