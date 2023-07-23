import vampytest

from ..getters import (
    ERROR_MESSAGE_APPENDIX, RETURN_TYPE_EXCEPTION, RETURN_TYPE_VALUE, RETURN_TYPE_WARNING, _get_env,
    _handle_get_env_generator, _process_int_env, _process_str_env
)

    
def iter_options__get_env():
    yield (
        'koishi',
        None,
        'str',
        _process_str_env,
        True,
        False,
        None,
        [
            (RETURN_TYPE_EXCEPTION, f'Environmental variable {"koishi"!r} is missing. {ERROR_MESSAGE_APPENDIX}'),
        ],
    )
    
    yield (
        'koishi',
        None,
        'str',
        _process_str_env,
        False,
        False,
        None,
        [
            (RETURN_TYPE_VALUE, None),
        ],
    )
    
    yield (
        'koishi',
        'satori',
        'str',
        _process_str_env,
        False,
        False,
        None,
        [
            (RETURN_TYPE_VALUE, 'satori'),
        ],
    )
    
    yield (
        'koishi',
        None,
        'str',
        _process_str_env,
        False,
        False,
        'orin',
        [
            (RETURN_TYPE_VALUE, 'orin'),
        ],
    )

    yield (
        'koishi',
        0,
        'int',
        _process_int_env,
        False,
        False,
        'okuu',
        [
            (RETURN_TYPE_WARNING, f'{"koishi"!r} is specified as non {"int"}: {"okuu"!r}, defaulting to {0!r}!'),
            (RETURN_TYPE_VALUE, 0),
        ],
    )

    yield (
        'koishi',
        None,
        'str',
        _process_str_env,
        True,
        False,
        '',
        [
            (
                RETURN_TYPE_EXCEPTION,
                f'Environmental variable {"koishi"!r} is specified as empty string. {ERROR_MESSAGE_APPENDIX}',
            ),
        ],
    )

    yield (
        'koishi',
        None,
        'str',
        _process_str_env,
        False,
        True,
        '',
        [
            (
                RETURN_TYPE_WARNING,
                f'Environmental variable {"koishi"!r} is specified as empty string. Defaulting to {None!r}!',
            ),
            (RETURN_TYPE_VALUE, None),
        ],
    )

    yield (
        'koishi',
        'satori',
        'str',
        _process_str_env,
        False,
        True,
        '',
        [
            (
                RETURN_TYPE_WARNING,
                f'Environmental variable {"koishi"!r} is specified as empty string. Defaulting to {"satori"!r}!',
            ),
            (RETURN_TYPE_VALUE, 'satori'),
        ],
    )

    yield (
        'koishi',
        'satori',
        'str',
        _process_str_env,
        False,
        False,
        '',
        [
            (RETURN_TYPE_VALUE, 'satori'),
        ],
    )

    yield (
        'koishi',
        None,
        'str',
        _process_str_env,
        False,
        False,
        'orin',
        [
            (RETURN_TYPE_VALUE, 'orin'),
        ],
    )


@vampytest._(vampytest.call_from(iter_options__get_env()).returning_last())
def test__get_env(
    name, default, accepted_type_name, accepted_processor, raise_if_missing_or_empty, warn_if_empty, value
):
    """
    Tests whether `_get_env` works as intended.
    
    
    Parameters
    ----------
    name : `str`
        The name of an environmental variable.
    default : `object`
        Default value to return.
    accepted_type_name : `str`
        The accepted type's name.
    accepted_type_processor : `(str) -> (bool, object)`
        Processor to process the environmental variable's value.
    raise_if_missing_or_empty : `bool`
        Whether exception should be thrown if the environmental variable is missing or empty.
    warn_if_empty : `bool`
        Whether warning should be dropped if empty environmental variable is received.
    value : `str`
        Value to return.
    
    Returns
    -------
    output : `str`
    """
    mocked = vampytest.mock_globals(_get_env, get_environmental_variable = lambda variable_name: value)
    return [*mocked(name, default, accepted_type_name, accepted_processor, raise_if_missing_or_empty, warn_if_empty)]


def test___handle_get_env_generator__return():
    """
    Tests whether ``_handle_get_env_generator`` works as intended.
    
    Case: return.
    """
    expected_output = 'pudding'
    
    def generator_function():
        nonlocal expected_output
        yield RETURN_TYPE_VALUE, expected_output
    
    output = _handle_get_env_generator(generator_function())
    
    vampytest.assert_eq(output, expected_output)


def test___handle_get_env_generator__error():
    """
    Tests whether ``_handle_get_env_generator`` works as intended.
    
    Case: error.
    """
    expected_output = 'pudding'
    
    def generator_function():
        nonlocal expected_output
        yield RETURN_TYPE_EXCEPTION, expected_output
    
    with vampytest.assert_raises(RuntimeError(expected_output)):
        _handle_get_env_generator(generator_function())


def test___handle_get_env_generator__warning():
    """
    Tests whether ``_handle_get_env_generator`` works as intended.
    
    Case: error.
    """
    expected_output_warn = 'pudding'
    expected_output_return = 'peach'
    warned_with = None
    
    def generator_function():
        nonlocal expected_output_warn
        nonlocal expected_output_return
        
        yield RETURN_TYPE_WARNING, expected_output_warn
        yield RETURN_TYPE_VALUE, expected_output_return
    
    def warn(message, *, stacklevel = 0):
        nonlocal warned_with
        warned_with = message
    
    mocked = vampytest.mock_globals(_handle_get_env_generator, warn = warn)
    
    output = mocked(generator_function())
    
    vampytest.assert_is(output, expected_output_return)
    vampytest.assert_eq(warned_with, expected_output_warn)
