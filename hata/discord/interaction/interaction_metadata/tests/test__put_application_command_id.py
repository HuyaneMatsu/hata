import vampytest

from ..fields import put_application_command_id


def _iter_options():
    application_command_id = 202308250002
    
    yield (
        0,
        False,
        {
            'data': {
                'id': None,
            },
        },
    )
    
    yield (
        0,
        True,
        {
            'data': {
                'id': None,
            },
        },
    )
    
    yield (
        application_command_id,
        False,
        {
            'data': {
                'id': str(application_command_id),
            },
        },
    )
    
    yield (
        application_command_id,
        True,
        {
            'data': {
                'id': str(application_command_id),
            },
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_application_command_id(input_value, defaults):
    """
    Tests whether ``put_application_command_id`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        The value to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_application_command_id(input_value, {}, defaults)
