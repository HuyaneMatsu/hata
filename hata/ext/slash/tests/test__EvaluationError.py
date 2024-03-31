import vampytest

from ..expression_parser import EvaluationError, HighlightGroup


def _assert_fields_set(exception):
    """
    Asserts whether ``EvaluationError`` has every of its attributes set.
    
    Parameters
    ----------
    exception : ``EvaluationError``
        The exception to test.
    """
    vampytest.assert_instance(exception, EvaluationError)
    vampytest.assert_instance(exception._pretty_repr, str, nullable = True)
    vampytest.assert_instance(exception.array, tuple)
    vampytest.assert_instance(exception.highlight_groups, list)
    vampytest.assert_instance(exception.message, str)


def test__EvaluationError__new():
    """
    Tests whether ``EvaluationError.__new__`` works as intended.
    """
    array = (*'hey mister'.encode(),)
    highlight_groups = [HighlightGroup(0, 3, False), HighlightGroup(3, 4, True)]
    message = 'have you seen my sister?'
    
    exception = EvaluationError(
        array,
        highlight_groups.copy(),
        message,
    )
    _assert_fields_set(exception)
    
    vampytest.assert_eq(exception.array, array)
    vampytest.assert_eq(exception.highlight_groups, highlight_groups)
    vampytest.assert_eq(exception.message, message)


def _iter_options__pretty_repr():
    yield (
        (
            (*'hey mister'.encode(),),
            [HighlightGroup(0, 3, False), HighlightGroup(3, 4, True)],    
            'have you seen my sister?',
        ),
        (
            'Evaluation failed: have you seen my sister?\n'
            '```\n'
            'hey mister\n'
            '~~~^\n'
            '```'
        ),
    )
    
    yield (
        (
            (49, 48, 40, 50, 48, 41),    
            [ HighlightGroup(0, 2, False), HighlightGroup(2, 3, True)],
            'decimal integer cannot be followed by parentheses start.',
        ),
        (
            'Evaluation failed: decimal integer cannot be followed by parentheses start.\n'
            '```\n'
            '10(20)\n'
            '~~^\n'
            '```'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__pretty_repr()).returning_last())
def test__EvaluationError__pretty_repr(parameters):
    """
    Tests whether ``EvaluationError.pretty_repr`` works as intended.
    
    Parameters
    ----------
    parameters : `tuple<object>`
        Parameters to create the exception from.
    
    Returns
    -------
    output : `str`
    """
    exception = EvaluationError(*parameters)
    
    output = exception.pretty_repr
    vampytest.assert_instance(output, str)
    return output


def test__EvaluationError__repr():
    """
    Tests whether ``EvaluationError.__repr__`` works as intended.
    """
    text = 'hey mister'
    array = [*text.encode()]
    highlight_groups = [HighlightGroup(0, 3, False), HighlightGroup(3, 4, True)]
    message = 'have you seen my sister?'
    
    exception = EvaluationError(
        array,
        highlight_groups,
        message,
    )
    
    output = repr(exception)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_in(type(exception).__name__, output)
    vampytest.assert_in(f'text = {text!r}', output)
    vampytest.assert_in(f'highlight_groups = {highlight_groups!r}', output)
    vampytest.assert_in(f'message = {message!r}', output)


def _iter_options__eq__same_type():
    yield (
        (
            (*'hey mister'.encode(),),
            [HighlightGroup(0, 3, False), HighlightGroup(3, 4, True)],    
            'have you seen my sister?',
        ),
        (
            (*'hey mister'.encode(),),
            [HighlightGroup(0, 3, False), HighlightGroup(3, 4, True)],    
            'have you seen my sister?',
        ),
        True,
    )
    
    yield (
        (
            (*'hey sister'.encode(),),
            [HighlightGroup(0, 3, False), HighlightGroup(3, 4, True)],    
            'have you seen my sister?',
        ),
        (
            (*'hey mister'.encode(),),
            [HighlightGroup(0, 3, False), HighlightGroup(3, 4, True)],    
            'have you seen my sister?',
        ),
        False,
    )
    
    yield (
        (
            (*'hey mister'.encode(),),
            [HighlightGroup(0, 3, False)],    
            'have you seen my sister?',
        ),
        (
            (*'hey mister'.encode(),),
            [HighlightGroup(0, 3, False), HighlightGroup(3, 4, True)],    
            'have you seen my sister?',
        ),
        False,
    )
    
    yield (
        (
            (*'hey mister'.encode(),),
            [HighlightGroup(0, 3, False), HighlightGroup(3, 4, True)],    
            'have you seen my mister?',
        ),
        (
            (*'hey mister'.encode(),),
            [HighlightGroup(0, 3, False), HighlightGroup(3, 4, True)],    
            'have you seen my sister?',
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq__same_type()).returning_last())
def test__EvaluationError__eq__same_type(parameters_0, parameters_1):
    """
    Tests whether ``EvaluationError.__eq__`` works as intended.
    
    Case: same type.
    
    Parameters
    ----------
    parameters_0 : `tuple<object>`
        Parameters to create exception from.
    parameters_0 : `tuple<object>`
        Parameters to create exception from.
    
    Returns
    -------
    output : `bool`
    """
    exception_0 = EvaluationError(*parameters_0)
    exception_1 = EvaluationError(*parameters_1)
    
    output = exception_0 == exception_1
    vampytest.assert_instance(output, bool)
    return output



def _iter_options__eq__different_type():
    yield None, False
    yield object(), False


@vampytest._(vampytest.call_from(_iter_options__eq__different_type()).returning_last())
def test__EvaluationError__eq__different_type(other):
    """
    Tests whether ``EvaluationError.__eq__`` works as intended.
    
    Case: different type.
    
    Parameters
    ----------
    other : `object`
        Other object to compare the exception to.
    
    Returns
    -------
    output : `bool`
    """
    array = (*'hey mister'.encode(),)
    highlight_groups = [HighlightGroup(0, 3, False), HighlightGroup(3, 4, True)]
    message = 'have you seen my sister?'
    
    exception = EvaluationError(
        array,
        highlight_groups,
        message,
    )
    
    output = exception == other
    vampytest.assert_instance(output, bool)
    return output


def test__EvaluationError__hash():
    """
    Tests whether ``EvaluationError.__hash__`` works as intended.
    """
    array = (*'hey mister'.encode(),)
    highlight_groups = [HighlightGroup(0, 3, False), HighlightGroup(3, 4, True)]
    message = 'have you seen my sister?'
    
    exception = EvaluationError(
        array,
        highlight_groups,
        message,
    )
    
    output = hash(exception)
    vampytest.assert_instance(output, int)


def test__EvaluationError__text():
    """
    Tests whether ``EvaluationError.text`` works as intended.
    """
    text = 'hey mister'
    array = [*text.encode()]
    highlight_groups = [HighlightGroup(0, 3, False), HighlightGroup(3, 4, True)]
    message = 'have you seen my sister?'
    
    exception = EvaluationError(
        array,
        highlight_groups,
        message,
    )
    
    output = exception.text
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, text)
