import vampytest

from ..preinstanced_meta import _get_name_default


class TestType():
    __slots__ = ()
    NAME_DEFAULT = 'mister'


def _iter_options__passing():
    yield None, ..., 'UNDEFINED'
    yield None, 'koishi', 'koishi'
    yield TestType, ..., 'mister'
    yield TestType, 'koishi', 'koishi'


def _iter_options__type_error():
    yield None, 12
    yield TestType, 12


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__get_name_default(type_parent, default_name):
    """
    Tests whether ``_get_name_default`` works as intended.
    
    Parameters
    ----------
    type_parent : `None | type`
        Parent type.
    
    default_name : `str | ...`
        The passed default name.
    
    Returns
    -------
    output : `str`
    
    Raises
    ------
    TypeError
    """
    output = _get_name_default(type_parent, default_name)
    vampytest.assert_instance(output, str)
    return output
