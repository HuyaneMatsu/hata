import vampytest

from ..preinstanced import Oauth2Scope


def test__Oauth2Scope__name():
    """
    Tests whether ``Oauth2Scope`` instance names are all strings.
    """
    for instance in Oauth2Scope.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__Oauth2Scope__value():
    """
    Tests whether ``Oauth2Scope`` instance values are all the expected value type.
    """
    for instance in Oauth2Scope.INSTANCES.values():
        vampytest.assert_instance(instance.value, Oauth2Scope.VALUE_TYPE)
