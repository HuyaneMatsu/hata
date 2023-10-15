import vampytest

from ....component import ComponentType

from ..fields import parse_component_type


def _iter_options():
    yield {}, ComponentType.none
    yield {'component_type': ComponentType.button.value}, ComponentType.button


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_component_type(input_data):
    """
    Tests whether ``parse_component_type`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``ComponentType``
    """
    output = parse_component_type(input_data)
    vampytest.assert_instance(output, ComponentType)
    return output
