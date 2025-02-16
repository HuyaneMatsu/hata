import vampytest

from ..fields import put_target_application_id


def _iter_options():
    application_id = 202308060051
    
    yield 0, False, {}
    yield 0, True, {'target_application_id': None}
    yield application_id, False, {'target_application_id': str(application_id)}
    yield application_id, True, {'target_application_id': str(application_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_target_application_id(input_value, defaults):
    """
    Tests whether ``put_target_application_id`` works as intended.
    
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
    return put_target_application_id(input_value, {}, defaults)
