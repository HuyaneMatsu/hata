import vampytest

from ..fields import put_features_into
from ..preinstanced import GuildFeature


def test__put_features_into():
    """
    Tests whether ``put_features_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {'features': []}),
        (
            (GuildFeature.animated_banner, GuildFeature.animated_icon,),
            True,
            {'features': [GuildFeature.animated_banner.value, GuildFeature.animated_icon.value]},
        ),
    ):
        data = put_features_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
