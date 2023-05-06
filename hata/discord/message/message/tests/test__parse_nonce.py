import vampytest

from ..fields import parse_nonce


def test__parse_nonce():
    """
    Tests whether ``parse_nonce`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'nonce': None}, None),
        ({'nonce': ''}, None),
        ({'nonce': 'Okuu'}, 'Okuu'),
    ):
        output = parse_nonce(input_data)
        vampytest.assert_eq(output, expected_output)
