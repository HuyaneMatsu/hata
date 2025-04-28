import vampytest

from ....guild import GuildFeature

from ..fields import validate_features


def _iter_options__passing():
    yield (
        None,
        None,
    )
    yield (
        [],
        None,
    )
    yield (
        GuildFeature.animated_banner,
        (GuildFeature.animated_banner, ),
    )
    yield (
        GuildFeature.animated_banner.value,
        (GuildFeature.animated_banner, ),
    )
    yield (
        [GuildFeature.animated_banner],
        (GuildFeature.animated_banner, ),
    )
    yield (
        [GuildFeature.animated_banner.value],
        (GuildFeature.animated_banner, ),
    )
    yield (
        [GuildFeature.animated_icon, GuildFeature.animated_banner],
        (GuildFeature.animated_banner, GuildFeature.animated_icon,),
    )
    yield (
        [GuildFeature.animated_banner, GuildFeature.animated_icon],
        (GuildFeature.animated_banner, GuildFeature.animated_icon,),
    )


def _iter_options__type_error():
    yield 12.6
    

@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_features(input_value):
    """
    Tests whether `validate_features` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | tuple<GuildFeature>`
    
    Raises
    ------
    TypeError
    """
    output = validate_features(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    return output

