import vampytest

from ..preinstanced import GuildFeature


@vampytest.call_from(GuildFeature.INSTANCES.values())
def test__GuildFeature__instances(instance):
    """
    Tests whether ``GuildFeature`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``GuildFeature``
        The instance to test.
    """
    vampytest.assert_instance(instance, GuildFeature)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, GuildFeature.VALUE_TYPE)
