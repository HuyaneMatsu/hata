import vampytest

from ...guild import GuildFeature

from ..fields import parse_features


def test__parse_features():
    """
    Tests whether ``parse_features`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'features': None}, None),
        ({'features': []}, None),
        ({'features': [GuildFeature.banner.value]}, (GuildFeature.banner,)),
    ):
        output = parse_features(input_data)
        vampytest.assert_eq(output, expected_output)
