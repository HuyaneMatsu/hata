import vampytest

from ..preinstanced import ApplicationCommandOptionType


def test__ApplicationCommandOptionType__name():
    """
    Tests whether ``ApplicationCommandOptionType`` instance names are all strings.
    """
    for instance in ApplicationCommandOptionType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__ApplicationCommandOptionType__value():
    """
    Tests whether ``ApplicationCommandOptionType`` instance values are all the expected value type.
    """
    for instance in ApplicationCommandOptionType.INSTANCES.values():
        vampytest.assert_instance(instance.value, ApplicationCommandOptionType.VALUE_TYPE)
