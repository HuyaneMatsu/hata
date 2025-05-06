import vampytest

from ..preinstance import Preinstance
from ..preinstanced_base import PreinstancedBase


def _assert_fields_set(preinstanced, *, value_type = ...):
    """
    Asserts whether every fields are set of the given preinstanced.
    
    Parameters
    ----------
    preinstanced : ``PreinstancedBase``
        The preinstanced to check.
    
    value_type : `type`, Optional (Keyword only)
        Value type to check for.
    """
    vampytest.assert_instance(preinstanced, PreinstancedBase)
    vampytest.assert_instance(preinstanced.name, str)
    vampytest.assert_instance(preinstanced.value, (object if value_type is ... else value_type))


def test__PreinstancedBase__new():
    """
    Tests whether ``PreinstancedBase.__new__`` works as intended.
    """
    value_type = int
    
    class TestPreinstance(PreinstancedBase, value_type = value_type):
        koishi = Preinstance(12, 'eye')
    
    # access
    koishi = TestPreinstance.koishi
    _assert_fields_set(koishi, value_type = value_type)
    
    vampytest.assert_eq(
        TestPreinstance.INSTANCES,
        {
            koishi.value: koishi,
        }
    )
    
    # access
    output = TestPreinstance(12)
    _assert_fields_set(output, value_type = value_type)
    vampytest.assert_is(output, koishi)
    
    vampytest.assert_eq(
        TestPreinstance.INSTANCES,
        {
            koishi.value: koishi,
        }
    )


def test__PreinstancedBase__new__name_default():
    """
    Tests whether ``PreinstancedBase.__new__`` works as intended.
    
    Case: name default.
    """
    value_type = int
    value = 12
    
    class TestPreinstance(PreinstancedBase, value_type = value_type):
        pass
    
    # access
    output = TestPreinstance(value)
    _assert_fields_set(output, value_type = value_type)
    vampytest.assert_eq(output.value, value)
    vampytest.assert_eq(output.name, TestPreinstance.NAME_DEFAULT)
    
    vampytest.assert_eq(
        TestPreinstance.INSTANCES,
        {
            value: output,
        }
    )


def test__PreinstancedBase__new__name_from_value():
    """
    Tests whether ``PreinstancedBase.__new__`` works as intended.
    
    Case: name from value.
    """
    value_type = str
    value = 'koishi'
    
    class TestPreinstance(PreinstancedBase, value_type = value_type):
        pass
    
    
    # access
    output = TestPreinstance(value)
    _assert_fields_set(output, value_type = value_type)
    vampytest.assert_eq(output.value, value)
    vampytest.assert_eq(output.name, value)
    
    vampytest.assert_eq(
        TestPreinstance.INSTANCES,
        {
            value: output,
        }
    )


def test__PreinstancedBase__eq():
    """
    Tests whether ``PreinstancedBase.__new__`` works as intended.
    """
    value_type = int
    
    class TestPreinstance(PreinstancedBase, value_type = int):
        koishi = Preinstance(12, 'eye')
        satori = Preinstance(13, 'mind')
        orin = Preinstance(14, 'cart')
        okuu = Preinstance(15, 'bomb')
    
    to_sort = [
        TestPreinstance.koishi,
        TestPreinstance.satori,
        TestPreinstance.orin,
        TestPreinstance.okuu,
        TestPreinstance.okuu,
        TestPreinstance.orin,
        TestPreinstance.satori,
        TestPreinstance.koishi,
    ]
    to_sort.sort()
    
    expected_output = [
        TestPreinstance.koishi,
        TestPreinstance.koishi,
        TestPreinstance.satori,
        TestPreinstance.satori,
        TestPreinstance.orin,
        TestPreinstance.orin,
        TestPreinstance.okuu,
        TestPreinstance.okuu,
    ]
    
    vampytest.assert_eq(
        to_sort,
        expected_output,
    )


def test__PreinstancedBase__hash():
    """
    Tests whether ``PreinstancedBase.__hash__`` works as intended.
    """
    value_type = int
    
    class TestPreinstance(PreinstancedBase, value_type = value_type):
        koishi = Preinstance(12, 'eye')
     
    output = hash(TestPreinstance.koishi)
    vampytest.assert_instance(output, int)


def test__PreinstancedBase__repr():
    """
    Tests whether ``PreinstancedBase.__repr__`` works as intended.
    """
    value_type = int
    
    value = 12
    name = 'eye'
    
    class TestPreinstance(PreinstancedBase, value_type = value_type):
        koishi = Preinstance(value, name)
     
    output = repr(TestPreinstance.koishi)
    vampytest.assert_instance(output, str)
    vampytest.assert_in(TestPreinstance.__name__, output)
    vampytest.assert_in(f'value = {value!r}', output)
    vampytest.assert_in(f'name = {name!r}', output)


def test__PreinstancedBase__sort():
    """
    Tests whether ``PreinstancedBase`` working works as intended.
    """
    value_type = int
    
    class TestPreinstance(PreinstancedBase, value_type = int):
        koishi = Preinstance(12, 'eye')
        satori = Preinstance(14, 'mind')
    
    to_sort = [
        TestPreinstance.koishi,
        TestPreinstance.satori,
        11,
        13,
        15,
        15,
        13,
        11,
        TestPreinstance.satori,
        TestPreinstance.koishi,
    ]
    to_sort.sort()
    
    expected_output = [
        11,
        11,
        TestPreinstance.koishi,
        TestPreinstance.koishi,
        13,
        13,
        TestPreinstance.satori,
        TestPreinstance.satori,
        15,
        15
    ]
    
    vampytest.assert_eq(to_sort, expected_output)
