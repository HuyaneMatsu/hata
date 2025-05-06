import vampytest

from ...activity import Activity, ActivityType, ActivityAssets
from ...utils import is_url

from ..urls import CDN_ENDPOINT, activity_asset_image_large_url_as


def _iter_options():
    application_id = 202504170050
    image_large = '566666'
    yield (
        application_id,
        ActivityAssets(image_large = image_large),
        {},
        f'{CDN_ENDPOINT}/app-assets/{application_id}/{image_large}.png'
    )
    
    application_id = 0
    image_large = '566666'
    yield (
        application_id,
        ActivityAssets(image_large = image_large),
        {},
        None,
    )
    
    application_id = 202504170051
    image_large = 'reisen'
    yield (
        application_id,
        ActivityAssets(image_large = image_large),
        {},
        None,
    )
    
    application_id = 202504170052
    yield (
        application_id,
        None,
        {},
        None,
    )
    
    application_id = 202504170053
    image_large = '566666'
    yield (
        application_id,
        ActivityAssets(image_large = image_large),
        {'ext': 'jpg', 'size': 128},
        f'{CDN_ENDPOINT}/app-assets/{application_id}/{image_large}.jpg?size=128'
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__activity_asset_image_large_url_as(application_id, activity_assets, keyword_parameters):
    """
    Tests whether ``activity_asset_image_large_url_as`` works as intended.
    
    Parameters
    ----------
    application_id : `int`
        Application identifier.
    
    activity_assets : `None | ActivityAssets`
        Assets to create the activity with.
    
    Returns
    -------
    output : `None | str`
    """
    activity = Activity(
        'pudding',
        activity_type = ActivityType.playing,
        application_id = application_id,
        assets = activity_assets,
    )
    
    output = activity_asset_image_large_url_as(activity, **keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    
    if (output is not None):
        vampytest.assert_true(is_url(output))
    
    return output
