import vampytest

from ..urls import DISCORD_ENDPOINT, build_name_plate_url_as


def _iter_options():
    asset_path = 'koishi/koishi/hat/'
    
    yield asset_path, True, f'{DISCORD_ENDPOINT}/assets/collectibles/{asset_path}asset.webm'
    yield asset_path, False, f'{DISCORD_ENDPOINT}/assets/collectibles/{asset_path}static.png'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_name_plate_url_as(asset_path, animated):
    """
    Tests whether ``build_name_plate_url_as`` works as intended.
    
    Parameters
    ----------
    asset_path : `str`
        Part to the name plate's asset.
    
    animated : `bool`
        Whether to return an url to an animated asset.
    
    Returns
    -------
    output : `str`
    """
    output = build_name_plate_url_as(asset_path, animated)
    vampytest.assert_instance(output, str)
    return output
