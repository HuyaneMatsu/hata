import vampytest

from ....guild import GuildFeature

from ..fields import validate_features


def _iter_options():
    yield None, None
    yield [], None
    yield GuildFeature.animated_banner, (GuildFeature.animated_banner, )
    yield GuildFeature.animated_banner.value, (GuildFeature.animated_banner, )
    yield [GuildFeature.animated_banner], (GuildFeature.animated_banner, )
    yield [GuildFeature.animated_banner.value], (GuildFeature.animated_banner, )
    yield (
        [GuildFeature.animated_banner, GuildFeature.animated_icon],
        (GuildFeature.animated_banner, GuildFeature.animated_icon,),
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__validate_features__0(input_value):
    """
    Tests whether `validate_features` works as intended.
    
    Case: passing.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Returns
    -------
    output : `None | tuple<GuildFeature>
    """
    return validate_features(input_value)


@vampytest.raising(TypeError)
@vampytest.call_with(12.6)
def test__validate_features__type_error(input_value):
    """
    Tests whether `validate_features` works as intended.
    
    Case: `TypeError`.
    
    Parameters
    ----------
    input_value : `object`
        The value to validate.
    
    Raises
    ------
    TypeError
    """
    validate_features(input_value)
