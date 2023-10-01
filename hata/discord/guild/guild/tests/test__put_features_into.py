import vampytest

from ..fields import put_features_into
from ..preinstanced import GuildFeature


def _iter_options():
    yield (None, False, {'features': []})
    yield (None, True, {'features': []})
    yield (
        (
            GuildFeature.animated_banner,
            GuildFeature.animated_icon,
        ),
        False,
        {
            'features': [
                GuildFeature.animated_banner.value,
                GuildFeature.animated_icon.value,
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_features_into(input_value, defaults):
    """
    Tests whether ``put_features_into`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | tuple<GuildFeature>`
        The value to serialise.
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_features_into(input_value, {}, defaults)
