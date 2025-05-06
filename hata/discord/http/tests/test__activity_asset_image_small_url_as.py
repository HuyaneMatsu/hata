import vampytest

from ...activity import Activity, ActivityType, ActivityAssets
from ...utils import is_url

from ..urls import CDN_ENDPOINT, activity_asset_image_small_url_as


def _iter_options():
    application_id = 202504170070
    image_small = '566666'
    yield (
        application_id,
        ActivityAssets(image_small = image_small),
        {},
        f'{CDN_ENDPOINT}/app-assets/{application_id}/{image_small}.png'
    )
    
    application_id = 0
    image_small = '566666'
    yield (
        application_id,
        ActivityAssets(image_small = image_small),
        {},
        None,
    )
    
    application_id = 202504170071
    image_small = 'reisen'
    yield (
        application_id,
        ActivityAssets(image_small = image_small),
        {},
        None,
    )
    
    application_id = 202504170072
    yield (
        application_id,
        None,
        {},
        None,
    )
    
    application_id = 202504170073
    image_small = '566666'
    yield (
        application_id,
        ActivityAssets(image_small = image_small),
        {'ext': 'jpg', 'size': 128},
        f'{CDN_ENDPOINT}/app-assets/{application_id}/{image_small}.jpg?size=128'
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__activity_asset_image_small_url_as(application_id, activity_assets, keyword_parameters):
    """
    Tests whether ``activity_asset_image_small_url_as`` works as intended.
    
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
    
    output = activity_asset_image_small_url_as(activity, **keyword_parameters)
    vampytest.assert_instance(output, str, nullable = True)
    
    if (output is not None):
        vampytest.assert_true(is_url(output))
    
    return output
