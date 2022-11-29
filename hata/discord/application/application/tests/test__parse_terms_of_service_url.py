import vampytest

from ..fields import parse_terms_of_service_url


def test__parse_terms_of_service_url():
    """
    Tests whether ``parse_terms_of_service_url`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'terms_of_service_url': None}, None),
        ({'terms_of_service_url': ''}, None),
        ({'terms_of_service_url': 'https://orindance.party/'}, 'https://orindance.party/'),
    ):
        output = parse_terms_of_service_url(input_data)
        vampytest.assert_eq(output, expected_output)
