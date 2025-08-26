import vampytest

from ..preinstanced import SessionPlatformType


def _assert_fields_set(status):
    """
    Asserts whether every field are set of the given session platform.
    
    Parameters
    ----------
    status : ``SessionPlatformType``
        The instance to test.
    """
    vampytest.assert_instance(status, SessionPlatformType)
    vampytest.assert_instance(status.name, str)
    vampytest.assert_instance(status.value, SessionPlatformType.VALUE_TYPE)


@vampytest.call_from(SessionPlatformType.INSTANCES.values())
def test__SessionPlatformType__instances(instance):
    """
    Tests whether ``SessionPlatformType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``SessionPlatformType``
        The instance to test.
    """
    _assert_fields_set(instance)
