import vampytest

from ..helpers import _nullable_list_difference


def _iter_options():
    yield None, None, None
    yield [1], None, {1}
    yield None, [1], None
    yield [1], [1], None
    yield [1, 2], [1, 3], {2}
    yield [2], [3], {2}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__nullable_list_difference(list_0, list_1):
    """
    Tests whether ``_nullable_list_difference`` works as intended.
    
    Parameters
    ----------
    list_0 : `None | list`
        Input list.
    list_1 : `None | list`
        Input list.
    
    Returns
    -------
    output : `None | set`
    """
    output = _nullable_list_difference(list_0, list_1)
    vampytest.assert_instance(output, list, nullable = True)
    if (output is not None):
        return {*output}
