import vampytest

from ..urls import DISCORD_ENDPOINT, build_name_plate_url


def _iter_options():
    asset_path = 'koishi/koishi/hat/'
    
    yield asset_path, f'{DISCORD_ENDPOINT}/assets/collectibles/{asset_path}asset.webm'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_name_plate_url(asset_path):
    """
    Tests whether ``build_name_plate_url`` works as intended.
    
    Parameters
    ----------
    asset_path : `str`
        Part to the name plate's asset.
    
    Returns
    -------
    output : `str`
    """
    output = build_name_plate_url(asset_path)
    vampytest.assert_instance(output, str)
    return output
