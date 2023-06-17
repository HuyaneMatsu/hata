import vampytest

from ..fields import parse_vanity_code


def test__parse_vanity_code():
    """
    Tests whether ``parse_vanity_code`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'vanity_url_code': None}, None),
        ({'vanity_url_code': ''}, None),
        ({'vanity_url_code': 'a'}, 'a'),
    ):
        output = parse_vanity_code(input_data)
        vampytest.assert_eq(output, expected_output)
