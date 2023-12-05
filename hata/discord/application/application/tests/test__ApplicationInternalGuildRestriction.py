import vampytest

from ..preinstanced import ApplicationInternalGuildRestriction


@vampytest.call_from(ApplicationInternalGuildRestriction.INSTANCES.values())
def test__ApplicationInternalGuildRestriction__instances(instance):
    """
    Tests whether ``ApplicationInternalGuildRestriction`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``ApplicationInternalGuildRestriction``
        The instance to test.
    """
    vampytest.assert_instance(instance, ApplicationInternalGuildRestriction)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, ApplicationInternalGuildRestriction.VALUE_TYPE)
