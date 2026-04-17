import vampytest

from ..urls import CDN_ENDPOINT, build_activity_asset_image_invite_cover_url


def _iter_options():
    application_id = 202511110000
    image_invite_cover = '566666'
    yield (
        application_id,
        image_invite_cover,
        f'{CDN_ENDPOINT}/app-assets/{application_id}/{image_invite_cover}.png',
    )
    
    application_id = 0
    image_invite_cover = '566666'
    yield (
        application_id,
        image_invite_cover,
        None,
    )
    
    application_id = 202511110001
    image_invite_cover = 'reisen'
    yield (
        application_id,
        image_invite_cover,
        None,
    )
    
    application_id = 202511110002
    image_invite_cover = None
    yield (
        application_id,
        image_invite_cover,
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_activity_asset_image_invite_cover_url(application_id, image_invite_cover):
    """
    Tests whether ``build_activity_asset_image_invite_cover_url`` works as intended.
    
    Parameters
    ----------
    application_id : `int`
        The activity's application's identifier.
    
    image_invite_cover : `None | str`
        The activity's asset's invite_cover image's value.
    
    Returns
    -------
    output : `None | str`
    """
    output = build_activity_asset_image_invite_cover_url(application_id, image_invite_cover)
    vampytest.assert_instance(output, str, nullable = True)
    
    return output
