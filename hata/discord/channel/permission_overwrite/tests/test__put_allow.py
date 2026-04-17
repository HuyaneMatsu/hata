import vampytest

from ....permission import Permission

from ..fields import put_allow


def _iter_options():
    yield Permission(), False, {'allow': '0'}
    yield Permission(), True, {'allow': '0'}
    yield Permission(1111), False, {'allow': '1111'}
    yield Permission(1111), True, {'allow': '1111'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_allow(input_value, default):
    """
    Tests whether ``put_allow`` works as intended.
    
    Parameters
    ----------
    input_value : ``Permission``
        The permission to put into the
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_allow(input_value, {}, True)
