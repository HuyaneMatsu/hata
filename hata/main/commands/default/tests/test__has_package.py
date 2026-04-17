import vampytest

from ..profiling import has_package


def _iter_options():
    yield 'shlex', True
    yield 'importlib', True,
    yield '__os__', False


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__has_package(input_value):
    """
    Tests whether ``has_package`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        Value to test with.
    
    Returns
    -------
    output : `bool`
    """
    output = has_package(input_value)
    vampytest.assert_instance(output, bool)
    return output
