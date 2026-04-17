import vampytest

from ....interaction import InteractionType

from ..fields import parse_type


def _iter_options():
    yield {}, InteractionType.none
    yield {'type': InteractionType.application_command.value}, InteractionType.application_command


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
    output : ``InteractionType``
    """
    output = parse_type(input_data)
    vampytest.assert_instance(output, InteractionType)
    return output
