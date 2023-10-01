import vampytest

from ...guild import GuildFeature

from ..fields import parse_features


def _iter_options():
    yield ({}, None)
    yield ({'features': None}, None)
    yield ({'features': []}, None)
    yield (
        {
            'features': [
                GuildFeature.animated_banner.value,
                GuildFeature.animated_icon.value,
            ],
        },
        (
            GuildFeature.animated_banner,
            GuildFeature.animated_icon,
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
    output : `None | tuple<GuildFeature>`
    """
    return parse_features(input_data)
