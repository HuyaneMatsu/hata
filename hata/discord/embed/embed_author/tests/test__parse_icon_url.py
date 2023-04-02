import vampytest

from ..fields import parse_icon_url


def test__parse_icon_url():
    """
    Tests whether ``parse_icon_url`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'icon_url': None}, None),
        ({'icon_url': ''}, None),
        ({'icon_url': 'https://orindance.party/'}, 'https://orindance.party/'),
    ):
        output = parse_icon_url(input_data)
        vampytest.assert_eq(output, expected_output)
