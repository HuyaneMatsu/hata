import vampytest

from ..preinstanced import NsfwLevel


def test__NsfwLevel__name():
    """
    Tests whether ``NsfwLevel`` instance names are all strings.
    """
    for instance in NsfwLevel.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__NsfwLevel__value():
    """
    Tests whether ``NsfwLevel`` instance values are all the expected value type.
    """
    for instance in NsfwLevel.INSTANCES.values():
        vampytest.assert_instance(instance.value, NsfwLevel.VALUE_TYPE)


def test__NsfwLevel__nsfw():
    """
    Tests whether ``NsfwLevel`` instance `.nsfw` fields are all bools.
    """
    for instance in NsfwLevel.INSTANCES.values():
        vampytest.assert_instance(instance.nsfw, bool)
