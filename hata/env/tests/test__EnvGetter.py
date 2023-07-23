import vampytest

from ..env_getter import _build_error_message_all_sources, _build_error_message_single_source, EnvGetter
from ..getters import RETURN_TYPE_EXCEPTION, RETURN_TYPE_VALUE, RETURN_TYPE_WARNING


def test__EnvGetter__new():
    """
    Tests whether ``EnvGetter.__new__`` works as intended.
    """
    env = EnvGetter()
    vampytest.assert_instance(env, EnvGetter)
    vampytest.assert_instance(env._captured, list, nullable = True)
    vampytest.assert_instance(env._entered, int)


def test__EnvGetter__repr():
    """
    Tests whether ``EnvGetter.__repr__`` works as intended.
    """
    env = EnvGetter()
    
    vampytest.assert_instance(repr(env), str)
    
    with env:
        vampytest.assert_instance(repr(env), str)
    
    env._capture(RETURN_TYPE_EXCEPTION, 'koishi')
    vampytest.assert_instance(repr(env), str)


def test__EnvGetter__context__passing():
    """
    Tests whether ``EnvGetter`` as a context manager works as intended.
    
    Case: passing.
    """
    env = EnvGetter()
    vampytest.assert_false(env._entered)
    
    with env:
        vampytest.assert_true(env._entered)
    
    vampytest.assert_false(env._entered)
    vampytest.assert_is(env._captured, None)


def test__EnvGetter__context__warning():
    """
    Tests whether ``EnvGetter`` as a context manager works as intended.
    
    Case: Warning.
    """
    env = EnvGetter()
    warned = False
    raised = False
    
    def warn_mocked(message, *, stacklevel = 0):
        nonlocal warned
        warned = True
        
    exit_mocked = vampytest.mock_globals(EnvGetter.__exit__, warn = warn_mocked)
    
    try:
        env.__enter__()
        env._capture(RETURN_TYPE_WARNING, 'koishi')
    finally:
        try:
            exit_mocked(env, None, None, None)
        except RuntimeError:
            raised = True
    
    vampytest.assert_is(env._captured, None)
    vampytest.assert_true(warned)
    vampytest.assert_false(raised)


def test__EnvGetter__context__exception():
    """
    Tests whether ``EnvGetter`` as a context manager works as intended.
    
    Case: Exception.
    """
    env = EnvGetter()
    warned = False
    raised = False
    
    def warn_mocked(message, *, stacklevel = 0):
        nonlocal warned
        warned = True
        
    exit_mocked = vampytest.mock_globals(EnvGetter.__exit__, warn = warn_mocked)
    
    try:
        env.__enter__()
        env._capture(RETURN_TYPE_EXCEPTION, 'koishi')
    finally:
        try:
            exit_mocked(env, None, None, None)
        except RuntimeError:
            raised = True
    
    vampytest.assert_is(env._captured, None)
    vampytest.assert_false(warned)
    vampytest.assert_true(raised)


def test__EnvGetter__nested_context__exception():
    """
    Tests whether ``EnvGetter`` as a context manager works as intended.
    
    Case: Nested + Exception.
    """
    env = EnvGetter()
    warned = False
    raised = False
    
    def warn_mocked(message, *, stacklevel = 0):
        nonlocal warned
        warned = True
        
    exit_mocked = vampytest.mock_globals(EnvGetter.__exit__, warn = warn_mocked)
    
    try:
        env.__enter__()
        env.__enter__()
        
        env._capture(RETURN_TYPE_EXCEPTION, 'koishi')
    finally:
        exit_mocked(env, None, None, None)
            
        try:
            exit_mocked(env, None, None, None)
        except RuntimeError:
            raised = True
    
    vampytest.assert_is(env._captured, None)
    vampytest.assert_false(warned)
    vampytest.assert_true(raised)


@vampytest.call_with(EnvGetter.get_bool)
@vampytest.call_with(EnvGetter.get_int)
@vampytest.call_with(EnvGetter.get_str)
def test__EnvGetter__get_any__un_entered(getter):
    """
    Tests whether ``EnvGetter.get_bool`` works as intended.
    
    Case: un-entered.
    
    Parameters
    ----------
    getter : `FunctionType`
        The getter to use.
    """
    env = EnvGetter()
    value = ''
    
    def get_environmental_variable(variable_name):
        nonlocal value
        return value
    
    mocked = vampytest.mock_globals(getter, 2, get_environmental_variable = get_environmental_variable)
    
    try:
        mocked(env, 'koishi', raise_if_missing_or_empty = True)
    except RuntimeError:
        raised = True
    else:
        raised = False
    
    vampytest.assert_true(raised)


@vampytest.call_with(EnvGetter.get_bool)
@vampytest.call_with(EnvGetter.get_int)
@vampytest.call_with(EnvGetter.get_str)
def test__EnvGetter__get_any__entered(getter):
    """
    Tests whether ``EnvGetter.get_bool`` works as intended.
    
    Case: entered.
    
    Parameters
    ----------
    getter : `FunctionType`
        The getter to use.
    """
    env = EnvGetter()
    value = ''
    
    def get_environmental_variable(variable_name):
        nonlocal value
        return value
    
    mocked = vampytest.mock_globals(getter, 2, get_environmental_variable = get_environmental_variable)
    
    try:
        env.__enter__()
        
        try:
            mocked(env, 'koishi', raise_if_missing_or_empty = True)
        except RuntimeError:
            raised = True
        else:
            raised = False
        
        vampytest.assert_false(raised)
    
    finally:
        try:
            env.__exit__(None, None, None)
        except RuntimeError:
            raised = True
        else:
            raised = False
        
        vampytest.assert_true(raised)
    
    

def test__EnvGetter__handle__un_entered():
    """
    Tests whether ``EnvGetter._handle`` works as intended.
    
    Case: Un-entered.
    """
    def generator_function():
        yield RETURN_TYPE_EXCEPTION, 'koishi'
    
    env = EnvGetter()
    
    try:
        env._handle(generator_function(), None)
    except RuntimeError:
        raised = True
    else:
        raised = False
    
    vampytest.assert_true(raised)


def test__EnvGetter__handle__entered():
    """
    Tests whether ``EnvGetter._handle`` works as intended.
    
    Case: Entered.
    """
    def generator_function():
        yield RETURN_TYPE_EXCEPTION, 'koishi'
    
    env = EnvGetter()
    
    env.__enter__()
    
    try:
        env._handle(generator_function(), None)
    except RuntimeError:
        raised = True
    else:
        raised = False
    
    vampytest.assert_false(raised)
    
    vampytest.assert_eq(env._captured, [(RETURN_TYPE_EXCEPTION, 'koishi')])


def test__EnvGetter__handle_as_entered__return():
    """
    Tests whether ``EnvGetter._handle_as_entered`` works as intended.
    
    Case: Return.
    """
    expected_output = 'pudding'
    default = 'satori'
    
    def generator_function():
        nonlocal expected_output
        yield RETURN_TYPE_VALUE, expected_output
    
    env = EnvGetter()
    output = env._handle_as_entered(generator_function(), default)
    
    vampytest.assert_is(env._captured, None)
    vampytest.assert_eq(output, expected_output)


def test__EnvGetter__handle_as_entered__warning():
    """
    Tests whether ``EnvGetter._handle_as_entered`` works as intended.
    
    Case: Warning.
    """
    expected_output = 'pudding'
    default = 'satori'
    
    def generator_function():
        nonlocal expected_output
        yield RETURN_TYPE_WARNING, expected_output
    
    env = EnvGetter()
    output = env._handle_as_entered(generator_function(), default)
    
    vampytest.assert_eq(env._captured, [(RETURN_TYPE_WARNING, expected_output)])
    vampytest.assert_eq(output, default)


def test__EnvGetter__handle_as_entered__exception():
    """
    Tests whether ``EnvGetter._handle_as_entered`` works as intended.
    
    Case: Exception.
    """
    expected_output = 'pudding'
    default = 'satori'
    
    def generator_function():
        nonlocal expected_output
        yield RETURN_TYPE_EXCEPTION, expected_output
    
    env = EnvGetter()
    output = env._handle_as_entered(generator_function(), default)
    
    vampytest.assert_eq(env._captured, [(RETURN_TYPE_EXCEPTION, expected_output)])
    vampytest.assert_eq(output, default)


def test__EnvGetter___capture():
    """
    Tests whether ``EnvGetter._capture`` works as intended.
    """
    env = EnvGetter()
    
    env._capture(RETURN_TYPE_EXCEPTION, 'koishi')
    vampytest.assert_eq(env._captured, [(RETURN_TYPE_EXCEPTION, 'koishi')])

    env._capture(RETURN_TYPE_WARNING, 'satori')
    vampytest.assert_eq(env._captured, [(RETURN_TYPE_EXCEPTION, 'koishi'), (RETURN_TYPE_WARNING, 'satori')])


def _iter_options___get_aggregated_state():
    yield (
        [],
        (RETURN_TYPE_VALUE, None),
    )

    yield (
        [(RETURN_TYPE_EXCEPTION, 'koishi'),],
        (RETURN_TYPE_EXCEPTION, 'koishi'),
    )

    yield (
        [
            (RETURN_TYPE_EXCEPTION, 'koishi'),
            (RETURN_TYPE_EXCEPTION, 'satori'),
        ],
        (
            RETURN_TYPE_EXCEPTION,
            (
                'Occurred exceptions while getting environmental variables (2):\n'
                'koishi\n'
                'satori'
            ),
        ),
    )

    yield (
        [(RETURN_TYPE_WARNING, 'koishi'),],
        (RETURN_TYPE_WARNING, 'koishi'),
    )

    yield (
        [
            (RETURN_TYPE_WARNING, 'koishi'),
            (RETURN_TYPE_WARNING, 'satori'),
        ],
        (
            RETURN_TYPE_WARNING,
            (
                'Occurred warnings while getting environmental variables (2):\n'
                'koishi\n'
                'satori'
            ),
        ),
    )

    yield (
        [
            (RETURN_TYPE_WARNING, 'koishi'),
            (RETURN_TYPE_EXCEPTION, 'satori'),
        ],
        (
            RETURN_TYPE_EXCEPTION,
            (
                'Occurred exceptions while getting environmental variables (1):\n'
                'satori\n'
                '\n'
                'Additional warnings (1):\n'
                'koishi'
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options___get_aggregated_state()).returning_last())
def test__EnvGetter___get_aggregated_state(to_capture):
    """
    Tests whether ``EnvGetter._get_aggregated_state`` works as intended.
    
    Parameters
    ----------
    to_capture : `list<(int, str)>`
        Results to capture.
    
    Returns
    -------
    output : `(int, None | str)`
    """
    env = EnvGetter()
    for item in to_capture :
        env._capture(*item)
    
    return env._get_aggregated_state()


def test__build_error_message_single_source():
    """
    Tests whether ``_build_error_message_single_source`` works as intended.
    """
    output = _build_error_message_single_source(['koishi', 'satori'], 'exceptions')
    
    vampytest.assert_eq(
        output,
        (
            'Occurred exceptions while getting environmental variables (2):\n'
            'koishi\n'
            'satori'
        ),
    )

def test__build_error_message_all_sources():
    """
    Tests whether ``_build_error_message_all_sources`` works as intended.
    """
    output = _build_error_message_all_sources(['satori'], ['koishi'])
    
    vampytest.assert_eq(
        output,
        (
            'Occurred exceptions while getting environmental variables (1):\n'
            'satori\n'
            '\n'
            'Additional warnings (1):\n'
            'koishi'
        ),
    )
