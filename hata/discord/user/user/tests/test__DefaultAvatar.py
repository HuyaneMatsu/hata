import vampytest

from ....color import Color
from ....utils import is_url

from ...user import User

from ..preinstanced import DefaultAvatar


def _assert_fields_set(default_avatar):
    """
    Asserts whether every field are set of the given default avatar.
    
    Parameters
    ----------
    default_avatar : ``DefaultAvatar``
        The instance to test.
    """
    vampytest.assert_instance(default_avatar, DefaultAvatar)
    vampytest.assert_instance(default_avatar.name, str)
    vampytest.assert_instance(default_avatar.value, DefaultAvatar.VALUE_TYPE)
    vampytest.assert_instance(default_avatar.color, Color)


@vampytest.call_from(DefaultAvatar.INSTANCES.values())
def test__DefaultAvatar__instances(instance):
    """
    Tests whether ``DefaultAvatar`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``DefaultAvatar``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__DefaultAvatar__new__min_fields():
    """
    Tests whether ``DefaultAvatar.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 6
    
    try:
        output = DefaultAvatar(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, DefaultAvatar.NAME_DEFAULT)
        vampytest.assert_eq(output.color, Color())
        vampytest.assert_is(DefaultAvatar.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del DefaultAvatar.INSTANCES[value]
        except KeyError:
            pass


def test__DefaultAvatar__for():
    """
    Tests whether ``DefaultAvatar.for_`` works as intended.
    """
    user = User.precreate(202211110018)
    default_avatar = DefaultAvatar.for_(user)
    
    vampytest.assert_instance(default_avatar, DefaultAvatar)


def test__DefaultAvatar__repr():
    """
    Tests whether ``DefaultAvatar.__repr__`` works as intended.
    """
    vampytest.assert_instance(repr(DefaultAvatar.blue), str)


def test__DefaultAvatar__url():
    """
    Tests whether ``DefaultAvatar.url`` works as intended.
    """
    vampytest.assert_true(is_url(DefaultAvatar.blue.url))


def test__DefaultAvatar__for__discriminator_deprecation():
    """
    Tests whether ``DefaultAvatar.for_`` handles discrimination deprecation as intended.
    """
    key = 1
    user_id_0 = 202305160000
    user_id_1 = 202305160001
    user_0 = User.precreate((user_id_0 & ((1 << 22) - 1)) | (key << 22))
    user_1 = User.precreate(user_id_1, discriminator = key)
    
    default_avatar_0 = DefaultAvatar.for_(user_0)
    default_avatar_1 = DefaultAvatar.for_(user_1)
    
    vampytest.assert_is(default_avatar_0, default_avatar_1)
