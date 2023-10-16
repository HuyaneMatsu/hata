import vampytest

from ...activity_assets import ActivityAssets

from ..fields import put_assets_into


def _iter_options():
    assets = ActivityAssets(image_large = 'hell')
    
    yield (None, False, {})
    yield (None, True, {'assets': None})
    yield (assets, False, {'assets': assets.to_data()})
    yield (assets, True, {'assets': assets.to_data(defaults = True)})


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_assets_into(input_value, defaults):
    """
    Tests whether ``put_assets_into`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | ActivityAssets`
        Value to serialise.
    defaults : `bool`
        Whether fields with their default value should be included.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_assets_into(input_value, {}, defaults)
