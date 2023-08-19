import vampytest

from ....permission import Permission

from ..fields import put_deny_into


def _iter_options():
    yield Permission(), False, {'deny': '0'}
    yield Permission(), True, {'deny': '0'}
    yield Permission(1111), False, {'deny': '1111'}
    yield Permission(1111), True, {'deny': '1111'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_deny_into(input_value, default):
    """
    Tests whether ``put_deny_into`` works as intended.
    
    Parameters
    ----------
    input_value : ``Permission``
        The permission to put into the
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_deny_into(input_value, {}, True)
