import vampytest

from ...entity_select_default_value import EntitySelectDefaultValue, EntitySelectDefaultValueType

from ..fields import put_default_values_into


def _iter_options():
    option_0 = EntitySelectDefaultValue(EntitySelectDefaultValueType.user, 202310130002)
    option_1 = EntitySelectDefaultValue(EntitySelectDefaultValueType.role, 202310130003)
    
    yield (None, False, {'default_values': []})
    yield (None, True, {'default_values': []})
    yield (
        (option_0, option_1),
        False,
        {'default_values': [option_0.to_data(), option_1.to_data()]},
    )
    yield (
        (option_0, option_1),
        True,
        {'default_values': [option_0.to_data(defaults = True), option_1.to_data(defaults = True)]},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_default_values_into(input_value, defaults):
    """
    Tests whether ``put_default_values_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<EntitySelectDefaultValue>`
        Input value.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_default_values_into(input_value, {}, defaults)
