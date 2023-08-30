import vampytest

from ..eula import EULA

from .test__EULA__constructor import _assert_fields_set


def test__EULA__copy():
    """
    Tests whether ``EULA.copy`` works as intended.
    """
    content = 'kimi'
    name = 'Red'
    
    eula = EULA(
        content = content,
        name = name,
    )
    
    copy = eula.copy()
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, eula)
    vampytest.assert_not_is(copy, eula)


def test__EULA__copy_with__0():
    """
    Tests whether ``EULA.copy_with`` works as intended.
    
    Case: No parameters given.
    """
    content = 'kimi'
    name = 'Red'
    
    eula = EULA(
        content = content,
        name = name,
    )
    
    copy = eula.copy_with()
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, eula)
    vampytest.assert_not_is(copy, eula)


def test__EULA__copy_with__1():
    """
    Tests whether ``EULA.copy_with`` works as intended.
    
    Case: Stuffed.
    """
    old_content = 'kimi'
    new_content = 'kiseki'
    old_name = 'Red'
    new_name = 'Angel'
    
    eula = EULA(
        content = old_content,
        name = old_name,
    )
    
    copy = eula.copy_with(
        content = new_content,
        name = new_name,
    )
    _assert_fields_set(copy)
    vampytest.assert_not_is(copy, eula)

    vampytest.assert_eq(copy.content, new_content)
    vampytest.assert_eq(copy.name, new_name)


def test__EULA__partial():
    """
    Tests whether ``EULA.accepted`` works as intended.
    """
    eula_id = 202211260013
    
    eula = EULA()
    vampytest.assert_true(eula.partial)
    
    
    eula = EULA.precreate(eula_id)
    vampytest.assert_false(eula.partial)
