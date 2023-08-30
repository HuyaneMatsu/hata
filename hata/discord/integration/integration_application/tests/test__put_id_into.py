import vampytest

from ..fields import put_id_into


def _iter_options():
    integration_application_id = 202212170046
    
    yield 0, False, {'id': None}
    yield 0, True, {'id': None}
    yield integration_application_id, False, {'id': str(integration_application_id)}
    yield integration_application_id, True, {'id': str(integration_application_id)}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_id_into(input_value, defaults):
    """
    Tests whether ``put_id_into`` works as intended.
    
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
    return put_id_into(input_value, {}, defaults)
