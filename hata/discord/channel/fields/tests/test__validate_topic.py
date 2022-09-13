import vampytest

from ..topic import validate_topic


def test__validate_topic():
    """
    Tests whether `validate_topic` works as intended.
    """
    for input_value, expected_output in (
        (None, None),
        ('', None),
        ('a', 'a'),
    ):
        output = validate_topic(input_value)
        vampytest.assert_eq(output, expected_output)
