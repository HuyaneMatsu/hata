import vampytest

from ..expression_parser import EvaluationError, LIMIT_FACTORIAL_MAX, HighlightGroup, evaluate_text


def _iter_options():
    # --- factorial ---
    
    yield (
        'factorial -> negative',
        'factorial(-1.0)',
        0,
        EvaluationError(
            (*(ord(character) for character in 'factorial(-1.0)'),),
            [
                HighlightGroup(0, 15, True),
            ],
            'Factorial is not defined for negative values: factorial(-1.0)',
        )
    )
    
    yield (
        'factorial -> non-integer',
        'factorial(0.5)',
        0,
        EvaluationError(
            (*(ord(character) for character in 'factorial(0.5)'),),
            [
                HighlightGroup(0, 14, True),
            ],
            'Factorial only accepts integral values: factorial(0.5)',
        )
    )
    
    yield (
        'factorial -> over limit',
        f'factorial({LIMIT_FACTORIAL_MAX + 1})',
        0,
        EvaluationError(
            (*(ord(character) for character in f'factorial({LIMIT_FACTORIAL_MAX + 1})'),),
            [
                HighlightGroup(0, 11 + len(str(LIMIT_FACTORIAL_MAX + 1)), True),
            ],
            f'Factorial over {LIMIT_FACTORIAL_MAX} is disallowed: factorial({LIMIT_FACTORIAL_MAX + 1})',
        )
    )
    
    yield (
        'factorial -> zero',
        'factorial(0)',
        1,
        None,
    )
    
    yield (
        'factorial -> positive',
        'factorial(4.0)',
        24,
        None,
    )
    
    # --- sqrt ---
    
    yield (
        'sqrt -> negative',
        'sqrt(-1.0)',
        0.0,
        EvaluationError(
            (*(ord(character) for character in 'sqrt(-1.0)'),),
            [
                HighlightGroup(0, 10, True),
            ],
            'Square root is not defined for negative values: sqrt(-1.0)',
        )
    )
    
    yield (
        'sqrt -> zero',
        'sqrt(0.0)',
        0.0,
        None,
    )
    
    yield (
        'sqrt -> positive',
        'sqrt(4.0)',
        2.0,
        None,
    )
    
    # ---- floor ----
    
    yield (
        'floor -> inf',
        'floor(inf)',
        0,
        EvaluationError(
            (*(ord(character) for character in 'floor(inf)'),),
            [
                HighlightGroup(0, 10, True),
            ],
            f'Floor rounding is not defined for infinite values: floor(inf)',
        )
    )
    
    yield (
        'floor -> -inf',
        'floor(-inf)',
        0,
        EvaluationError(
            (*(ord(character) for character in 'floor(-inf)'),),
            [
                HighlightGroup(0, 11, True),
            ],
            f'Floor rounding is not defined for infinite values: floor(-inf)',
        )
    )
    
    yield (
        'floor -> zero',
        'floor(0.0)',
        0,
        None,
    )
    
    yield (
        'floor -> positive',
        'floor(4.6)',
        4,
        None,
    )
    
    yield (
        'floor -> negative',
        'floor(-4.6)',
        -5,
        None,
    )
    
    # ---- ceil ----
    
    yield (
        'ceil -> inf',
        'ceil(inf)',
        0,
        EvaluationError(
            (*(ord(character) for character in 'ceil(inf)'),),
            [
                HighlightGroup(0, 9, True),
            ],
            f'Ceil rounding is not defined for infinite values: ceil(inf)',
        )
    )
    
    yield (
        'ceil -> -inf',
        'ceil(-inf)',
        0,
        EvaluationError(
            (*(ord(character) for character in 'ceil(-inf)'),),
            [
                HighlightGroup(0, 10, True),
            ],
            f'Ceil rounding is not defined for infinite values: ceil(-inf)',
        )
    )
    
    yield (
        'ceil -> zero',
        'ceil(0.0)',
        0,
        None,
    )
    
    yield (
        'ceil -> positive',
        'ceil(4.6)',
        5,
        None,
    )
    
    yield (
        'ceil -> negative',
        'ceil(-4.6)',
        -4,
        None,
    )
    
    # ---- round ----
    
    yield (
        'round -> inf',
        'round(inf)',
        0,
        EvaluationError(
            (*(ord(character) for character in 'round(inf)'),),
            [
                HighlightGroup(0, 10, True),
            ],
            f'Rounding is not defined for infinite values: round(inf)',
        )
    )
    
    yield (
        'round -> -inf',
        'round(-inf)',
        0,
        EvaluationError(
            (*(ord(character) for character in 'round(-inf)'),),
            [
                HighlightGroup(0, 11, True),
            ],
            f'Rounding is not defined for infinite values: round(-inf)',
        )
    )
    
    yield (
        'round -> zero',
        'round(0.0)',
        0,
        None,
    )
    
    yield (
        'round -> positive',
        'round(4.6)',
        5,
        None,
    )
    
    yield (
        'round -> negative',
        'round(-4.6)',
        -5,
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first())
def test__evaluate_text(input_expression, expected_output, expected_exception):
    if expected_exception is None:
        output = evaluate_text(input_expression)
        vampytest.assert_is(type(output), type(expected_output))
        vampytest.assert_eq(output, expected_output)
    
    else:
        with vampytest.assert_raises(expected_exception):
            evaluate_text(input_expression)
