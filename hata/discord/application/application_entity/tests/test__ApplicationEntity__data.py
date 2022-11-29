import vampytest

from ..application_entity import ApplicationEntity

from .test__ApplicationEntity__constructor import _assert_is_every_attribute_set


def test__ApplicationEntity__from_data():
    """
    Tests whether ``ApplicationEntity.from_data`` works as intended.
    
    Case: Default.
    """
    application_entity_id = 202211240047
    name = 'Red'
    
    data = {
        'id': str(application_entity_id),
        'name': name,
    }
    
    application_entity = ApplicationEntity.from_data(data)
    _assert_is_every_attribute_set(application_entity)
    vampytest.assert_eq(application_entity.id, application_entity_id)
    
    vampytest.assert_eq(application_entity.name, name)


def test__ApplicationEntity__to_data():
    """
    Tests whether ``ApplicationEntity.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    application_entity_id = 202211240048
    name = 'Red'
    
    expected_output = {
        'id': str(application_entity_id),
        'name': name,
    }
    
    application_entity = ApplicationEntity.precreate(
        application_entity_id,
        name = name,
    )
    
    vampytest.assert_eq(application_entity.to_data(defaults = True, include_internals = True), expected_output)
