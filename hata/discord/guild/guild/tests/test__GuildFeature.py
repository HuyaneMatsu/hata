import vampytest

from ..preinstanced import GuildFeature


def test__GuildFeature__name():
    """
    Tests whether ``GuildFeature`` instance names are all strings.
    """
    for instance in GuildFeature.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__GuildFeature__value():
    """
    Tests whether ``GuildFeature`` instance values are all the expected value type.
    """
    for instance in GuildFeature.INSTANCES.values():
        vampytest.assert_instance(instance.value, GuildFeature.VALUE_TYPE)
