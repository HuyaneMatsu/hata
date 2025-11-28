import vampytest

from ..fields import validate_features
from ..preinstanced import GuildFeature


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
        GuildFeature.banner_animated,
        (GuildFeature.banner_animated, ),
    )
    yield (
        GuildFeature.banner_animated.value,
        (GuildFeature.banner_animated, ),
    )
    yield (
        [GuildFeature.banner_animated],
        (GuildFeature.banner_animated, ),
    )
    yield (
        [GuildFeature.banner_animated.value],
        (GuildFeature.banner_animated, ),
    )
    yield (
        [GuildFeature.icon_animated, GuildFeature.banner_animated],
        (GuildFeature.banner_animated, GuildFeature.icon_animated,),
    )
    yield (
        [GuildFeature.banner_animated, GuildFeature.icon_animated],
        (GuildFeature.banner_animated, GuildFeature.icon_animated,),
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
    output :  ``None | tuple<GuildFeature>``
    
    Raises
    ------
    TypeError
    """
    output = validate_features(input_value)
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, GuildFeature)
    
    return output
