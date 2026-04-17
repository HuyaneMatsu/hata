import vampytest

from ....guild import GuildFeature

from ..fields import put_features


def _iter_options():
    yield (
        None,
        False,
        {
            'features': [],
        },
    )
    
    yield (
        None,
        True,
        {
            'features': [],
        },
    )
    
    yield (
        (
            GuildFeature.banner_animated,
            GuildFeature.icon_animated,
        ),
        False,
        {
            'features': [
                GuildFeature.banner_animated.value,
                GuildFeature.icon_animated.value,
            ],
        },
    )
    
    yield (
        (
            GuildFeature.banner_animated,
            GuildFeature.icon_animated,
        ),
        True,
        {
            'features': [
                GuildFeature.banner_animated.value,
                GuildFeature.icon_animated.value,
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_features(input_value, defaults):
    """
    Tests whether ``put_features`` is working as intended.
    
    Parameters
    ----------
    input_value :  ``None | tuple<GuildFeature>``
        The value to serialise.
    
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_features(input_value, {}, defaults)
