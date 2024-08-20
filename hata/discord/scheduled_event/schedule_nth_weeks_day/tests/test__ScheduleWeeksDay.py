import vampytest

from ..preinstanced import ScheduleWeeksDay


@vampytest.call_from(ScheduleWeeksDay.INSTANCES.values())
def test__ScheduleWeeksDay__instances(instance):
    """
    Tests whether ``ScheduleWeeksDay`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ScheduleWeeksDay``
        The instance to test.
    """
    vampytest.assert_instance(instance, ScheduleWeeksDay)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ScheduleWeeksDay.VALUE_TYPE)
