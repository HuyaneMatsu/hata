import vampytest

from ..fields import put_application_id


def _iter_options():
    application_id = 202310010005

    yield 0, False, {'application_id': None}
    yield 0, True, {'application_id': None}
    yield application_id, False, {'application_id': str(application_id)}
    yield application_id, True, {'application_id': str(application_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_application_id(input_value, defaults):
    """
    Tests whether ``put_application_id`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        The value to serialise.
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_application_id(input_value, {}, defaults)
