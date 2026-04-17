import vampytest

from ..application_entity import ApplicationEntity


def test__ApplicationEntity__repr():
    """
    Tests whether ``ApplicationEntity.__repr__`` works as intended.
    
    Case: include defaults and internals.
    """
    application_entity_id = 202211240049
    name = 'Red'
    
    
    application_entity = ApplicationEntity.precreate(
        application_entity_id,
        name = name,
    )
    
    vampytest.assert_instance(repr(application_entity), str)


def test__ApplicationEntity__hash():
    """
    Tests whether ``ApplicationEntity.__hash__`` works as intended.
    
    Case: include defaults and internals.
    """
    application_entity_id = 202211240050
    name = 'Red'
    
    application_entity = ApplicationEntity.precreate(
        application_entity_id,
        name = name,
    )
    
    vampytest.assert_instance(hash(application_entity), int)


def test__ApplicationEntity__eq():
    """
    Tests whether ``ApplicationEntity.__eq__`` works as intended.
    
    Case: include defaults and internals.
    """
    application_entity_id = 202211240051
    name = 'Red'
    
    keyword_parameters = {
        'name': name,
    }
    
    application_entity = ApplicationEntity.precreate(application_entity_id, **keyword_parameters)
    
    vampytest.assert_eq(application_entity, application_entity)
    vampytest.assert_ne(application_entity, object())
    
    test_application_entity = ApplicationEntity(**keyword_parameters)
    vampytest.assert_eq(application_entity, test_application_entity)
    
    for field_name, field_value in (
        ('name', 'Suwako'),
    ):
        test_application_entity = ApplicationEntity(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(application_entity, test_application_entity)
