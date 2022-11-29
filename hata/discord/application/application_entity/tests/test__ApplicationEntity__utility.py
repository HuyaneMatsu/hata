import vampytest

from ..application_entity import ApplicationEntity

from .test__ApplicationEntity__constructor import _assert_is_every_attribute_set


def test__ApplicationEntity__copy():
    """
    Tests whether ``ApplicationEntity.copy`` works as intended.
    """
    name = 'Red'
    
    
    application_entity = ApplicationEntity(
        name = name,
    )
    
    copy = application_entity.copy()
    _assert_is_every_attribute_set(copy)
    vampytest.assert_eq(copy, application_entity)
    vampytest.assert_not_is(copy, application_entity)


def test__ApplicationEntity__copy_with__0():
    """
    Tests whether ``ApplicationEntity.copy_with`` works as intended.
    
    Case: No parameters given.
    """
    name = 'Red'
    
    
    application_entity = ApplicationEntity(
        name = name,
    )
    
    copy = application_entity.copy_with()
    _assert_is_every_attribute_set(copy)
    vampytest.assert_eq(copy, application_entity)
    vampytest.assert_not_is(copy, application_entity)


def test__ApplicationEntity__copy_with__1():
    """
    Tests whether ``ApplicationEntity.copy_with`` works as intended.
    
    Case: Stuffed.
    """
    old_name = 'Red'
    new_name = 'Angel'
    
    
    application_entity = ApplicationEntity(
        name = old_name,
    )
    
    copy = application_entity.copy_with(
        name = new_name,
    )
    _assert_is_every_attribute_set(copy)
    vampytest.assert_not_is(copy, application_entity)

    vampytest.assert_eq(copy.name, new_name)


def test__ApplicationEntity__partial():
    """
    Tests whether ``ApplicationEntity.accepted`` works as intended.
    """
    application_entity_id = 202211240052
    
    application_entity = ApplicationEntity()
    vampytest.assert_true(application_entity.partial)
    
    
    application_entity = ApplicationEntity.precreate(application_entity_id)
    vampytest.assert_false(application_entity.partial)
