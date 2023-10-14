import vampytest

from ...entity_select_default_value import EntitySelectDefaultValue, EntitySelectDefaultValueType

from ..fields import parse_default_values


def _iter_options():
    option_0 = EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310130000)
    option_1 = EntitySelectDefaultValue(EntitySelectDefaultValueType.role, 202310130001)
    
    yield ({}, None)
    yield ({'default_values': None}, None)
    yield ({'default_values': []}, None)
    yield ({'default_values': [option_0.to_data()]}, (option_0, ))
    yield ({'default_values': [option_0.to_data(), option_1.to_data()]}, (option_0, option_1))


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_default_values(input_data):
    """
    Tests whether ``parse_default_values`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<EntitySelectDefaultValue>`
    """
    return parse_default_values(input_data)
