import vampytest

from ..fields import parse_features
from ..preinstanced import GuildFeature


def test__parse_features():
    """
    Tests whether ``parse_features`` works as intended.
    """
    for input_data, expected_output in (
        ({}, None),
        ({'features': None}, None),
        ({'features': []}, None),
        (
            {'features': [GuildFeature.animated_banner.value, GuildFeature.animated_icon.value]},
            (GuildFeature.animated_banner, GuildFeature.animated_icon,),
        ),
    ):
        output = parse_features(input_data)
        vampytest.assert_eq(output, expected_output)
