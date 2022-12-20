import vampytest

from ..fields import validate_features
from ..preinstanced import GuildFeature


def test__validate_features__0():
    """
    Tests whether `validate_features` works as intended.
    
    Case: passing.
    """
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ([GuildFeature.animated_banner], (GuildFeature.animated_banner, )),
        ([GuildFeature.animated_banner.value], (GuildFeature.animated_banner, )),
        (
            [GuildFeature.animated_banner, GuildFeature.animated_icon],
            (GuildFeature.animated_banner, GuildFeature.animated_icon,),
        ),
    ):
        output = validate_features(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_features__1():
    """
    Tests whether `validate_features` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_features(input_value)
