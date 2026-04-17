import vampytest

from ..preinstanced import ScheduleFrequency


@vampytest.call_from(ScheduleFrequency.INSTANCES.values())
def test__ScheduleFrequency__instances(instance):
    """
    Tests whether ``ScheduleFrequency`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ScheduleFrequency``
        The instance to test.
    """
    vampytest.assert_instance(instance, ScheduleFrequency)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ScheduleFrequency.VALUE_TYPE)
