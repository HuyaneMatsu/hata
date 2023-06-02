import vampytest

from ..helpers import _validate_bot


def test__validate_bot__passing():
    """
    Tests whether ``_validate_bot`` is working as intended.
    
    Case: Passing.
    """
    for input_value, expected_output in (
        (('aya',), (['aya'], None)),
        (('aya', 'ya'), (['aya', 'ya'], None)),
    ):
        output = _validate_bot(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_bot__failing():
    """
    Tests whether ``_validate_bot`` works as intended.
    
    Case: Failing.
    """
    for input_value in (
        (),
        ('aya', ''),
        ('123',),
        (' ',),
    ):
        output = _validate_bot(input_value)
        vampytest.assert_instance(output, tuple)
        vampytest.assert_eq(len(output), 2)
        vampytest.assert_is(output[0], None)
        vampytest.assert_instance(output[1], str)
