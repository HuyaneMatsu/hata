import vampytest

from ..urls import CDN_ENDPOINT, build_activity_asset_image_large_url


def _iter_options():
    application_id = 202504170040
    image_large = '566666'
    yield (
        application_id,
        image_large,
        f'{CDN_ENDPOINT}/app-assets/{application_id}/{image_large}.png',
    )
    
    application_id = 0
    image_large = '566666'
    yield (
        application_id,
        image_large,
        None,
    )
    
    application_id = 202504170041
    image_large = 'reisen'
    yield (
        application_id,
        image_large,
        None,
    )
    
    application_id = 202504170042
    image_large = None
    yield (
        application_id,
        image_large,
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_activity_asset_image_large_url(application_id, image_large):
    """
    Tests whether ``build_activity_asset_image_large_url`` works as intended.
    
    Parameters
    ----------
    application_id : `int`
        The activity's application's identifier.
    
    image_large : `None | str`
        The activity's asset's large image's value.
    
    Returns
    -------
    output : `None | str`
    """
    output = build_activity_asset_image_large_url(application_id, image_large)
    vampytest.assert_instance(output, str, nullable = True)
    
    return output
