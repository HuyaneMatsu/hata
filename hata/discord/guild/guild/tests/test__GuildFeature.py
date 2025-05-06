import vampytest

from ..preinstanced import GuildFeature


def _assert_fields_set(guild_feature):
    """
    Asserts whether every field are set of the given guild feature.
    
    Parameters
    ----------
    guild_feature : ``GuildFeature``
        The instance to test.
    """
    vampytest.assert_instance(guild_feature, GuildFeature)
    vampytest.assert_instance(guild_feature.name, str)
    vampytest.assert_instance(guild_feature.value, GuildFeature.VALUE_TYPE)


@vampytest.call_from(GuildFeature.INSTANCES.values())
def test__GuildFeature__instances(instance):
    """
    Tests whether ``GuildFeature`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``GuildFeature``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__GuildFeature__new__min_fields():
    """
    Tests whether ``GuildFeature.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 'NYANNERS_ONLY'
    
    try:
        output = GuildFeature(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, 'nyanners only')
        vampytest.assert_is(GuildFeature.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del GuildFeature.INSTANCES[value]
        except KeyError:
            pass
