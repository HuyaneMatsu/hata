import vampytest

from ..fields import parse_verify_key


def test__parse_verify_key():
    """
    Tests whether ``parse_verify_key`` works as intended.
    """
    for input_data, expected_output in (
        ({'verify_key': None}, None),
        ({'verify_key': ''}, None),
        ({'verify_key': 'a'}, 'a'),
    ):
        output = parse_verify_key(input_data)
        vampytest.assert_eq(output, expected_output)
