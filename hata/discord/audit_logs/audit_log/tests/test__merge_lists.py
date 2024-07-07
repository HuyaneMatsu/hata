import vampytest

from ..helpers import _merge_lists


def _iter_options():
    yield [], None
    yield [None, None], None
    yield [None, [6]], [6]
    yield [[5], None], [5]
    yield [[5], [6]], [5, 6]


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__merge_lists(input_value):
    """
    Tests whether ``_merge_lists`` works as intended.
    
    Parameters
    ----------
    input_value : `iterable<None | list>`
        Value to test with.
    
    Returns
    -------
    output : `None | list`
    """
    output = _merge_lists(input_value)
    vampytest.assert_instance(output, list, nullable = True)
    return output
