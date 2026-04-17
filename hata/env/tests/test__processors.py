import vampytest

from ..getters import _process_bool_env, _process_int_env, _process_str_env


def _iter_options__bool():
    yield '', (False, False)
    yield 'ayaya', (False, False)
    yield '0', (True, False)
    yield 'false', (True, False)
    yield 'fAlsE', (True, False)
    yield '1', (True, True)
    yield 'true', (True, True)
    yield 'tRuE', (True, True)
    

@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__process_bool_env(input_value):
    """
    Tests whether ``_process_bool_env`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        The value to process.
    
    Returns
    -------
    output : `(bool, bool)`
    """
    return _process_bool_env(input_value)


def _iter_options__str():
    yield '', (False, '')
    yield 'ayaya', (True, 'ayaya')


@vampytest._(vampytest.call_from(_iter_options__str()).returning_last())
def test__process_str_env(input_value):
    """
    Tests whether ``_process_str_env`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        The value to process.
    
    Returns
    -------
    output : `(bool, str)`
    """
    return _process_str_env(input_value)


def _iter_options__int():
    yield '', (False, 0)
    yield 'ayaya', (False, 0)
    yield '100', (True, 100)
    yield '+100', (True, 100)
    yield '-100', (True, -100)


@vampytest._(vampytest.call_from(_iter_options__int()).returning_last())
def test__process_int_env(input_value):
    """
    Tests whether ``_process_int_env`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        The value to process.
    
    Returns
    -------
    output : `(bool, int)`
    """
    return _process_int_env(input_value)
