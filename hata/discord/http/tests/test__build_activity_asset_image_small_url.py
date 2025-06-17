import vampytest

from ..urls import CDN_ENDPOINT, build_activity_asset_image_small_url


def _iter_options():
    application_id = 202504170060
    image_small = '566666'
    yield (
        application_id,
        image_small,
        f'{CDN_ENDPOINT}/app-assets/{application_id}/{image_small}.png',
    )
    
    application_id = 0
    image_small = '566666'
    yield (
        application_id,
        image_small,
        None,
    )
    
    application_id = 202504170061
    image_small = 'reisen'
    yield (
        application_id,
        image_small,
        None,
    )
    
    application_id = 202504170062
    image_small = None
    yield (
        application_id,
        image_small,
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_activity_asset_image_small_url(application_id, image_small):
    """
    Tests whether ``build_activity_asset_image_small_url`` works as intended.
    
    Parameters
    ----------
    application_id : `int`
        The activity's application's identifier.
    
    image_small : `None | str`
        The activity's asset's small image's value.
    
    Returns
    -------
    output : `None | str`
    """
    output = build_activity_asset_image_small_url(application_id, image_small)
    vampytest.assert_instance(output, str, nullable = True)
    return output
