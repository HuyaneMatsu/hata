import vampytest

from ..fields import put_features
from ..preinstanced import SKUFeature


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
            SKUFeature.single_player,
            SKUFeature.pvp,
        ),
        False,
        {
            'features': [
                SKUFeature.single_player.value,
                SKUFeature.pvp.value,
            ],
        },
    )
    
    yield (
        (
            SKUFeature.single_player,
            SKUFeature.pvp,
        ),
        True,
        {
            'features': [
                SKUFeature.single_player.value,
                SKUFeature.pvp.value,
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_features(input_value, defaults):
    """
    Tests whether ``put_features`` is working as intended.
    
    Parameters
    ----------
    input_value : ``None | tuple<SKUFeature>``
        The value to serialise.
    
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_features(input_value, {}, defaults)
