import vampytest

from ....color import Color
from ....utils import is_url

from ...user import User

from ..preinstanced import DefaultAvatar


def test__DefaultAvatar__name():
    """
    Tests whether ``DefaultAvatar`` instance names are all strings.
    """
    for instance in DefaultAvatar.INSTANCES.values():
        vampytest.assert_instance(instance.name, str)


def test__DefaultAvatar__value():
    """
    Tests whether ``DefaultAvatar`` instance values are all the expected value type.
    """
    for instance in DefaultAvatar.INSTANCES.values():
        vampytest.assert_instance(instance.value, DefaultAvatar.VALUE_TYPE)


def test__DefaultAvatar__Color():
    """
    Tests whether ``DefaultAvatar`` colors are all set correctly.
    """
    for instance in DefaultAvatar.INSTANCES.values():
        vampytest.assert_instance(instance.color, Color)


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
