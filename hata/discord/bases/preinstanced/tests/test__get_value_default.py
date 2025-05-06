import vampytest

from ..preinstanced_meta import _get_value_default


def _iter_options():
    yield type(None), None
    yield int, 0
    yield str, ''
    yield object, None


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_value_default(value_type):
    """
    Tests whether ``_get_value_default`` works as intended.
    
    Parameters
    ----------
    value_type : `type<NoneType | int | str>`
        The value's type.
    
    Returns
    -------
    output : `None | int | str`
    """
    return _get_value_default(value_type)
