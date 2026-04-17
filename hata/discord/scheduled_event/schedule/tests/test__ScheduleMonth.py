import vampytest

from ..preinstanced import ScheduleMonth


@vampytest.call_from(ScheduleMonth.INSTANCES.values())
def test__ScheduleMonth__instances(instance):
    """
    Tests whether ``ScheduleMonth`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ScheduleMonth``
        The instance to test.
    """
    vampytest.assert_instance(instance, ScheduleMonth)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ScheduleMonth.VALUE_TYPE)
