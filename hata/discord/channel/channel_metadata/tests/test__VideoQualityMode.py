import vampytest

from ..preinstanced import VideoQualityMode


def test__VideoQualityMode__name():
    """
    Tests whether ``VideoQualityMode`` instance names are all strings.
    """
    for instance in VideoQualityMode.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__VideoQualityMode__value():
    """
    Tests whether ``VideoQualityMode`` instance values are all the expected value type.
    """
    for instance in VideoQualityMode.INSTANCES.values():
        vampytest.assert_instance(instance.value, VideoQualityMode.VALUE_TYPE)
