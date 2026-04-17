import vampytest

from ..abort import CONVERSION_ABORT


def _iter_options__set_validator():
    yield object(), []
    yield None, [False]
    yield False, [False]
    yield True, [True]


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_ABORT__set_validator(input_value):
    """
    Tests whether ``CONVERSION_ABORT.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<bool>`
    """
    return [*CONVERSION_ABORT.set_validator(input_value)]
