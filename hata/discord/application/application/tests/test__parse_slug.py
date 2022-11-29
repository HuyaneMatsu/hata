import vampytest

from ..fields import parse_slug


def test__parse_slug():
    """
    Tests whether ``parse_slug`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'slug': None}, None),
        ({'slug': ''}, None),
        ({'slug': 'https://orindance.party/'}, 'https://orindance.party/'),
    ):
        output = parse_slug(input_data)
        vampytest.assert_eq(output, expected_output)
