import vampytest

from ..fields import put_id_into


def _iter_options():
    application_entity_id = 202211240042
    
    yield 0, False, {'id': None}
    yield 0, True, {'id': None}
    yield application_entity_id, False, {'id': str(application_entity_id)}
    yield application_entity_id, True, {'id': str(application_entity_id)}


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
