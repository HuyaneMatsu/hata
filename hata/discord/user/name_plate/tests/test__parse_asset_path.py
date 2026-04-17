import vampytest

from ..fields import parse_asset_path


def _iter_options():
    yield {}, ''
    yield {'asset': None}, ''
    yield {'asset': ''}, ''
    yield {'asset': 'nameplates/nameplates/cityscape/'}, 'nameplates/nameplates/cityscape/'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_asset_path(input_data):
    """
    Tests whether ``parse_asset_path`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse the name from.
    
    Returns
    -------
    name : `str`
    """
    output = parse_asset_path(input_data)
    vampytest.assert_instance(output, str)
    return output
