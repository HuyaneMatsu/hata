import vampytest

from ..eula import EULA

from .test__EULA__constructor import _assert_fields_set


def test__EULA__from_data__0():
    """
    Tests whether ``EULA.from_data`` works as intended.
    
    Case: Default.
    """
    eula_id = 202211260007
    content = 'kimi'
    name = 'Red'
    
    data = {
        'id': str(eula_id),
        'content': content,
        'name': name,
    }
    
    eula = EULA.from_data(data)
    _assert_fields_set(eula)
    vampytest.assert_eq(eula.id, eula_id)
    
    vampytest.assert_eq(eula.content, content)
    vampytest.assert_eq(eula.name, name)


def test__EULA__from_data__1():
    """
    Tests whether ``EULA.from_data`` works as intended.
    
    Case: Caching.
    """
    eula_id = 202211260008
    
    data = {
        'id': str(eula_id),
    }
    
    eula = EULA.from_data(data)
    test_eula = EULA.from_data(data)
    
    vampytest.assert_is(eula, test_eula)


def test__EULA__to_data():
    """
    Tests whether ``EULA.to_data`` works as intended.
    
    Case: include defaults and internals.
    """
    eula_id = 202211260009
    content = 'kimi'
    name = 'Red'
    
    expected_output = {
        'id': str(eula_id),
        'content': content,
        'name': name,
    }
    
    eula = EULA.precreate(
        eula_id,
        content = content,
        name = name,
    )
    
    vampytest.assert_eq(eula.to_data(defaults = True, include_internals = True), expected_output)
