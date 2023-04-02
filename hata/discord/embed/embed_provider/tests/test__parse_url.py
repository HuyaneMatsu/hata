import vampytest

from ..fields import parse_url


def test__parse_url():
    """
    Tests whether ``parse_url`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'url': None}, None),
        ({'url': ''}, None),
        ({'url': 'https://orindance.party/'}, 'https://orindance.party/'),
    ):
        output = parse_url(input_data)
        vampytest.assert_eq(output, expected_output)
