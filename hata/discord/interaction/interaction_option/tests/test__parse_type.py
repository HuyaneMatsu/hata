import vampytest

from ....application_command import ApplicationCommandOptionType

from ..fields import parse_type


def _iter_options():
    yield {}, ApplicationCommandOptionType.none
    yield {'type': ApplicationCommandOptionType.sub_command.value}, ApplicationCommandOptionType.sub_command


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_type(input_data):
    """
    Tests whether ``parse_type`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Input data.
    
    Returns
    -------
    output : ``ApplicationCommandOptionType``
    """
    output = parse_type(input_data)
    vampytest.assert_instance(output, ApplicationCommandOptionType)
    return output
