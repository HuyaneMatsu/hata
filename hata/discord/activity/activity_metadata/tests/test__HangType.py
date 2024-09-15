from types import FunctionType

import vampytest

from ..preinstanced import HangType


@vampytest.call_from(HangType.INSTANCES.values())
def test__HangType__instances(instance):
    """
    Tests whether ``HangType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``HangType``
        The instance to test.
    """
    vampytest.assert_instance(instance, HangType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, HangType.VALUE_TYPE)
    vampytest.assert_instance(instance.name_getter, FunctionType)
