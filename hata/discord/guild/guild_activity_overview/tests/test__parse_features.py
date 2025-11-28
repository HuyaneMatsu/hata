import vampytest

from ...guild import GuildFeature

from ..fields import parse_features


def _iter_options():
    yield (
        {},
        None,
    )
    yield (
        {
            'features': None,
        },
        None,
    )
    yield (
        {
            'features': [],
        },
        None,
    )
    yield (
        {
            'features': [
                GuildFeature.banner_animated.value,
                GuildFeature.icon_animated.value,
            ],
        },
        (
            GuildFeature.banner_animated,
            GuildFeature.icon_animated,
        ),
    )
    yield (
        {
            'features': [
                GuildFeature.icon_animated.value,
                GuildFeature.banner_animated.value,
            ],
        },
        (
            GuildFeature.banner_animated,
            GuildFeature.icon_animated,
        ),
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_features(input_data):
    """
    Tests whether ``parse_features`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output :  ``None | tuple<GuildFeature>``
    """
    output = parse_features(input_data)
    
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, GuildFeature)
    
    return output
