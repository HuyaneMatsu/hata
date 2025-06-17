import vampytest

from ....color import Color

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


def test__DefaultAvatar__repr():
    """
    Tests whether ``DefaultAvatar.__repr__`` works as intended.
    """
    vampytest.assert_instance(repr(DefaultAvatar.blue), str)


def _iter_options__url():
    yield DefaultAvatar.blue, True


@vampytest._(vampytest.call_from(_iter_options__url()).returning_last())
def test__DefaultAvatar__url(default_avatar):
    """
    Tests whether ``DefaultAvatar.url`` works as intended.
    
    Parameters
    ----------
    default_avatar : ``DefaultAvatar``
        Default avatar to get its url.
    
    Returns
    -------
    has_url : `bool`
    """
    output = default_avatar.url
    vampytest.assert_instance(output, str)
    return True
