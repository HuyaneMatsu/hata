import vampytest
from ..getters import get_bool_env, get_int_env, get_str_env


def _iter_options():
    yield (
        get_str_env,
        'koishi',
        None,
        True,
        False,
        None,
        None,
        False,
        True,
    )
    
    yield (
        get_str_env,
        'koishi',
        None,
        False,
        False,
        None,
        None,
        False,
        False,
    )
    
    yield (
        get_str_env,
        'koishi',
        'satori',
        False,
        False,
        None,
        'satori',
        False,
        False,
    )
    
    yield (
        get_str_env,
        'koishi',
        None,
        False,
        False,
        'orin',
        'orin',
        False,
        False,
    )

    yield (
        get_int_env,
        'koishi',
        0,
        False,
        False,
        'okuu',
        0,
        True,
        False,
    )

    yield (
        get_str_env,
        'koishi',
        None,
        True,
        False,
        '',
        None,
        False,
        True,
    )

    yield (
        get_str_env,
        'koishi',
        None,
        False,
        True,
        '',
        None,
        True,
        False,
    )

    yield (
        get_str_env,
        'koishi',
        'satori',
        False,
        True,
        '',
        'satori',
        True,
        False,
    )

    yield (
        get_str_env,
        'koishi',
        'satori',
        False,
        False,
        '',
        'satori',
        False,
        False,
    )

    yield (
        get_str_env,
        'koishi',
        None,
        False,
        False,
        'orin',
        'orin',
        False,
        False,
    )

    yield (
        get_int_env,
        'koishi',
        None,
        False,
        False,
        '-100',
        -100,
        False,
        False,
    )

    yield (
        get_bool_env,
        'koishi',
        None,
        False,
        False,
        'true',
        True,
        False,
        False,
    )


@vampytest.call_from(_iter_options())
def test__get_env__default(
    env_getter,
    name,
    default,
    raise_if_missing_or_empty,
    warn_if_empty,
    value,
    expected_output,
    expect_to_warn,
    expect_to_raise
):    
    warned = False
    
    def warn(message, *, stacklevel = 0):
        nonlocal warned
        warned = True
    
    def get_environmental_variable(variable_name):
        nonlocal value
        return value
    
    mocked = vampytest.mock_globals(env_getter, 2, warn = warn, get_environmental_variable = get_environmental_variable)
    
    try:
        output = mocked(
            name,
            default = default,
            raise_if_missing_or_empty = raise_if_missing_or_empty,
            warn_if_empty = warn_if_empty,
        )
    except RuntimeError:
        raised = True
        output = None
    else:
        raised = False
    
    vampytest.assert_eq(output, expected_output)
    vampytest.assert_eq(warned, expect_to_warn)
    vampytest.assert_eq(raised, expect_to_raise)
