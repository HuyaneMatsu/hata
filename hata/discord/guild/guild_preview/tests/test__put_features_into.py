import vampytest

from ....guild import GuildFeature

from ..fields import put_features_into


def test__put_features_into():
    """
    Tests whether ``put_features_into`` works as intended.
    """
    for input_value, defaults, expected_output in (
        (None, False, {'features': []}),
        ((GuildFeature.banner, ), True, {'features': [GuildFeature.banner.value]}),
    ):
        data = put_features_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
