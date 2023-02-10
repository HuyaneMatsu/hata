import vampytest

from ..fields import validate_shard_count


def test__validate_shard_count__0():
    """
    Tests whether `validate_shard_count` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (0, 0),
        (1, 0),
        (2, 2),
        (-1, 0),
    ):
        output = validate_shard_count(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_shard_count__1():
    """
    Tests whether `validate_shard_count` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_shard_count(input_value)
