import vampytest

from ..fields import parse_privacy_policy_url


def test__parse_privacy_policy_url():
    """
    Tests whether ``parse_privacy_policy_url`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'privacy_policy_url': None}, None),
        ({'privacy_policy_url': ''}, None),
        ({'privacy_policy_url': 'https://orindance.party/'}, 'https://orindance.party/'),
    ):
        output = parse_privacy_policy_url(input_data)
        vampytest.assert_eq(output, expected_output)
