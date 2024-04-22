import vampytest

from ...application_entity import ApplicationEntity

from ..fields import put_publishers_into


def _iter_options():
    application_entity_0 = ApplicationEntity.precreate(202404140004)
    application_entity_1 = ApplicationEntity.precreate(202404140005)
    
    yield (
        None,
        False,
        {
            'publishers': []
        },
    )
    
    yield (
        None,
        True,
        {
            'publishers': []
        },
    )
    
    yield (
        (application_entity_0, application_entity_1),
        False,
        {
            'publishers': [
                application_entity_0.to_data(defaults = False, include_internals = True),
                application_entity_1.to_data(defaults = False, include_internals = True),
            ]
        },
    )
    
    yield (
        (application_entity_0, application_entity_1),
        True,
        {
            'publishers': [
                application_entity_0.to_data(defaults = True, include_internals = True),
                application_entity_1.to_data(defaults = True, include_internals = True),
            ]
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_publishers_into(input_value, defaults):
    """
    Tests whether ``put_publishers_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<ApplicationEntity>`
        Value to serialise.
    defaults : `bool`
        Whether fields with their default values should be included as well.
    
    Returns
    -------    
    output : `dict<str, object>`
    """
    return put_publishers_into(input_value, {}, defaults, include_internals = True)
