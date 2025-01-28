import vampytest

from ..preinstanced import NsfwLevel


def _assert_fields_set(nsfw_level):
    """
    Asserts whether every field are set of the given nsfw level.
    
    Parameters
    ----------
    nsfw_level : ``NsfwLevel``
        The instance to test.
    """
    vampytest.assert_instance(nsfw_level, NsfwLevel)
    vampytest.assert_instance(nsfw_level.name, str)
    vampytest.assert_instance(nsfw_level.value, NsfwLevel.VALUE_TYPE)
    vampytest.assert_instance(nsfw_level.nsfw, bool)


@vampytest.call_from(NsfwLevel.INSTANCES.values())
def test__NsfwLevel__instances(instance):
    """
    Tests whether ``NsfwLevel`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``NsfwLevel``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__NsfwLevel__new__min_fields():
    """
    Tests whether ``NsfwLevel.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 30
    
    try:
        output = NsfwLevel(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, NsfwLevel.NAME_DEFAULT)
        vampytest.assert_eq(output.nsfw, True)
        vampytest.assert_is(NsfwLevel.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del NsfwLevel.INSTANCES[value]
        except KeyError:
            pass


def test__NsfwLevel__repr():
    """
    Tests whether ``NsfwLevel.__repr__`` works as intended.
    """
    nsfw_level = NsfwLevel.explicit
    
    output = repr(nsfw_level)
    vampytest.assert_instance(output, str)
    vampytest.assert_in(type(nsfw_level).__name__, output)
    vampytest.assert_in(f'value = {nsfw_level.value!r}', output)
    vampytest.assert_in(f'name = {nsfw_level.name!r}', output)
    vampytest.assert_in(f'nsfw = {nsfw_level.nsfw!r}', output)
