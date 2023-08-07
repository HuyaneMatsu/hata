import vampytest

from ....interaction import InteractionType

from ..fields import put_type_into


def _iter_options():
    yield InteractionType.application_command, False, {'type': InteractionType.application_command.value}
    yield InteractionType.application_command, True, {'type': InteractionType.application_command.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_type_into(input_value, defaults):
    """
    Tests whether ``put_type_into`` is working as intended.
    
    Parameters
    ----------
    input_value : ``InteractionType``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_type_into(input_value, {}, defaults)
