import vampytest

from ..fields import parse_rejection_reason


def test__parse_rejection_reason():
    """
    Tests whether ``parse_rejection_reason`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'rejection_reason': None}, None),
        ({'rejection_reason': ''}, None),
        ({'rejection_reason': 'a'}, 'a'),
    ):
        output = parse_rejection_reason(input_data)
        vampytest.assert_eq(output, expected_output)
