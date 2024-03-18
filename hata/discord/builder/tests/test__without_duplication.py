import vampytest

from ..builder_base import _without_duplication


def _iter_options():
    yield [1, 2, 3], [1, 2, 3]
    yield [1, 2, 1, 2], [1, 2]


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__without_duplication(elements):
    """
    Tests whether ``_without_duplication`` works as intended.
    
    Parameters
    ----------
    elements : `list`
        Elements to test on.
    
    Returns
    -------
    output : `list`
    """
    return _without_duplication(elements)
