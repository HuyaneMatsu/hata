import vampytest

from ..preinstanced import InteractionResponseType


def test__InteractionResponseType__name():
    """
    Tests whether ``InteractionResponseType`` instance names are all strings.
    """
    for instance in InteractionResponseType.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__InteractionResponseType__value():
    """
    Tests whether ``InteractionResponseType`` instance values are all the expected value type.
    """
    for instance in InteractionResponseType.INSTANCES.values():
        vampytest.assert_instance(instance.value, InteractionResponseType.VALUE_TYPE)
