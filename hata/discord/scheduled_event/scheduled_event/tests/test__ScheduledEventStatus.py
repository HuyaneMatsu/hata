import vampytest

from ..preinstanced import ScheduledEventStatus


@vampytest.call_from(ScheduledEventStatus.INSTANCES.values())
def test__ScheduledEventStatus__instances(instance):
    """
    Tests whether ``ScheduledEventStatus`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ScheduledEventStatus``
        The instance to test.
    """
    vampytest.assert_instance(instance, ScheduledEventStatus)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ScheduledEventStatus.VALUE_TYPE)
