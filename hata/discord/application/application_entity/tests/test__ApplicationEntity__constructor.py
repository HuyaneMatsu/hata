import vampytest

from ..application_entity import ApplicationEntity


def _assert_is_every_attribute_set(application_entity):
    """
    Asserts whether every attributes of the given are set.
    
    Parameters
    ----------
    application_entity : ``ApplicationEntity``
        The application_entity to check.
    """
    vampytest.assert_instance(application_entity, ApplicationEntity)
    vampytest.assert_instance(application_entity.id, int)
    vampytest.assert_instance(application_entity.name, str)


def test__ApplicationEntity__new__0():
    """
    Tests whether ``ApplicationEntity.__new__`` works as intended.
    
    Case: No parameters given.
    """
    application_entity = ApplicationEntity()
    _assert_is_every_attribute_set(application_entity)


def test__ApplicationEntity__new__1():
    """
    Tests whether ``ApplicationEntity.__new__`` works as intended.
    
    Case: All parameters given.
    """
    
    name = 'Red'
    
    application_entity = ApplicationEntity(
        name = name,
    )
    _assert_is_every_attribute_set(application_entity)
    
    vampytest.assert_eq(application_entity.name, name)



def test__ApplicationEntity__create_empty():
    """
    Tests whether ``ApplicationEntity._create_empty`` works as intended.
    """
    application_entity_id = 202211240044
    
    application_entity = ApplicationEntity._create_empty(application_entity_id)
    _assert_is_every_attribute_set(application_entity)
    vampytest.assert_eq(application_entity.id, application_entity_id)


def test__ApplicationEntity__precreate__0():
    """
    Tests whether ``ApplicationEntity.precreate`` works as intended.
    
    Case: No parameters given.
    """
    application_entity_id = 202211240045
    
    application_entity = ApplicationEntity.precreate(application_entity_id)
    _assert_is_every_attribute_set(application_entity)
    vampytest.assert_eq(application_entity.id, application_entity_id)


def test__ApplicationEntity__precreate__1():
    """
    Tests whether ``ApplicationEntity.precreate`` works as intended.
    
    Case: All parameters given.
    """
    application_entity_id = 202211240046
    name = 'Red'
    
    application_entity = ApplicationEntity.precreate(
        application_entity_id,
        name = name,
    )
    _assert_is_every_attribute_set(application_entity)
    vampytest.assert_eq(application_entity.id, application_entity_id)
    
    vampytest.assert_eq(application_entity.name, name)
