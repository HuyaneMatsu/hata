import vampytest

from ..preinstanced import GuildActivityOverviewActivityLevel


@vampytest.call_from(GuildActivityOverviewActivityLevel.INSTANCES.values())
def test__GuildActivityOverviewActivityLevel__instances(instance):
    """
    Tests whether ``GuildActivityOverviewActivityLevel`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``GuildActivityOverviewActivityLevel``
        The instance to test.
    """
    vampytest.assert_instance(instance, GuildActivityOverviewActivityLevel)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, GuildActivityOverviewActivityLevel.VALUE_TYPE)
