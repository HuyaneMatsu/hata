import vampytest

from ....application_command import ApplicationCommandOptionType

from ..fields import put_type


def _iter_options():
    yield ApplicationCommandOptionType.sub_command, False, {'type': ApplicationCommandOptionType.sub_command.value}
    yield ApplicationCommandOptionType.sub_command, True, {'type': ApplicationCommandOptionType.sub_command.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_type(input_value, defaults):
    """
    Tests whether ``put_type`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ApplicationCommandOptionType``
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_type(input_value, {}, defaults)
