import vampytest

from ..fields import put_rejection_reason_into


def test__put_rejection_reason_into():
    """
    Tests whether ``put_rejection_reason_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'rejection_reason': None}),
        ('a', False, {'rejection_reason': 'a'}),
    ):
        output = put_rejection_reason_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
