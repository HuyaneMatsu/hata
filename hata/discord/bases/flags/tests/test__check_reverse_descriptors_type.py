import vampytest

from ..flag_meta import _check_reverse_descriptors_type


def _iter_options__passing():
    yield True
    yield False


def _iter_options__type_error():
    yield None
    yield object()


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__check_reverse_descriptors_type(value):
    """
    Tests whether ``_check_reverse_descriptors_type`` works as intended.
    
    Parameters
    ----------
    value : `object`
        The value to check.
    
    Raises
    ------
    TypeError
    """
    _check_reverse_descriptors_type('nyan', value)
