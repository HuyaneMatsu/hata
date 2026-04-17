import vampytest

from ..eula import EULA


def test__EULA__repr():
    """
    Tests whether ``EULA.__repr__`` works as intended.
    
    Case: include defaults and internals.
    """
    eula_id = 202211260010
    content = 'kimi'
    name = 'Red'
    
    
    eula = EULA.precreate(
        eula_id,
        content = content,
        name = name,
    )
    
    vampytest.assert_instance(repr(eula), str)


def test__EULA__hash():
    """
    Tests whether ``EULA.__hash__`` works as intended.
    
    Case: include defaults and internals.
    """
    eula_id = 202211260011
    content = 'kimi'
    name = 'Red'
    
    eula = EULA.precreate(
        eula_id,
        content = content,
        name = name,
    )
    
    vampytest.assert_instance(hash(eula), int)


def test__EULA__eq():
    """
    Tests whether ``EULA.__eq__`` works as intended.
    
    Case: include defaults and internals.
    """
    eula_id = 202211260012
    content = 'kimi'
    name = 'Red'
    
    keyword_parameters = {
        'content': content,
        'name': name,
    }
    
    eula = EULA.precreate(eula_id, **keyword_parameters)
    
    vampytest.assert_eq(eula, eula)
    vampytest.assert_ne(eula, object())
    
    test_eula = EULA(**keyword_parameters)
    vampytest.assert_eq(eula, test_eula)
    
    for field_name, field_value in (
        ('content', 'kiseki'),
        ('name', 'Suwako'),
    ):
        test_eula = EULA(**{**keyword_parameters, field_name: field_value})
        vampytest.assert_ne(eula, test_eula)
