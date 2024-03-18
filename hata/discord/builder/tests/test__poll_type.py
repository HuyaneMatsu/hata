import vampytest

from ..conversion import _poll_type


def _iter_options__passing():
    yield type, (int, ), int
    yield type, (int, object), int
    yield type, (bool, object), bool


def _iter_options__type_error():
    yield type, (int, bool)
    yield Exception, (int, )
    yield Exception, (object,)


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__poll_type(meta_type, base_types):
    """
    Tests whether ``_poll_type`` works as intended.
    
    Parameters
    ----------
    meta_type : `type`
        Type we are sub-instantiating.
    base_types : `tuple<type>`
        Inherited types.
    
    Returns
    -------
    output : `type`
    
    Raises
    ------
    TypeError
    """
    return _poll_type(meta_type, 'mister', base_types)
