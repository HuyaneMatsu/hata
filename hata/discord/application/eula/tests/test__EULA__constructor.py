import vampytest

from ..eula import EULA


def _assert_fields_set(eula):
    """
    Asserts whether every attributes of the given are set.
    
    Parameters
    ----------
    eula : ``EULA``
        The eula to check.
    """
    vampytest.assert_instance(eula, EULA)
    vampytest.assert_instance(eula.content, str, nullable = True)
    vampytest.assert_instance(eula.id, int)
    vampytest.assert_instance(eula.name, str)


def test__EULA__new__0():
    """
    Tests whether ``EULA.__new__`` works as intended.
    
    Case: No parameters given.
    """
    eula = EULA()
    _assert_fields_set(eula)


def test__EULA__new__1():
    """
    Tests whether ``EULA.__new__`` works as intended.
    
    Case: All parameters given.
    """
    content = 'kimi'
    name = 'Red'
    
    eula = EULA(
        content = content,
        name = name,
    )
    _assert_fields_set(eula)
    
    vampytest.assert_eq(eula.content, content)
    vampytest.assert_eq(eula.name, name)



def test__EULA__create_empty():
    """
    Tests whether ``EULA._create_empty`` works as intended.
    """
    eula_id = 202211260003
    
    eula = EULA._create_empty(eula_id)
    _assert_fields_set(eula)
    vampytest.assert_eq(eula.id, eula_id)


def test__EULA__precreate__0():
    """
    Tests whether ``EULA.precreate`` works as intended.
    
    Case: No parameters given.
    """
    eula_id = 202211260004
    
    eula = EULA.precreate(eula_id)
    _assert_fields_set(eula)
    vampytest.assert_eq(eula.id, eula_id)


def test__EULA__precreate__1():
    """
    Tests whether ``EULA.precreate`` works as intended.
    
    Case: All parameters given.
    """
    eula_id = 202211260005
    content = 'kimi'
    name = 'Red'
    
    eula = EULA.precreate(
        eula_id,
        content = content,
        name = name,
    )
    _assert_fields_set(eula)
    vampytest.assert_eq(eula.id, eula_id)
    
    vampytest.assert_eq(eula.content, content)
    vampytest.assert_eq(eula.name, name)


def test__EULA__precreate__2():
    """
    Tests whether ``EULA.precreate`` works as intended.
    
    Case: Caching.
    """
    eula_id = 202211260006
    
    eula = EULA.precreate(eula_id)
    test_eula = EULA.precreate(eula_id)
    
    vampytest.assert_is(eula, test_eula)
