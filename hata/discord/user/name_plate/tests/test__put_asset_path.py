import vampytest

from ..fields import put_asset_path


def _iter_options():
    yield '', False, {'asset': ''}
    yield '', True, {'asset': ''}
    yield 'nameplates/nameplates/cityscape/', False, {'asset': 'nameplates/nameplates/cityscape/'}
    yield 'nameplates/nameplates/cityscape/', True, {'asset': 'nameplates/nameplates/cityscape/'}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_asset_path(input_value, defaults):
    """
    Tests whether ``put_asset_path`` works as intended.
    
    Parameters
    ----------
    input_value : `str`
        The value to serialise.
    
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_asset_path(input_value, {}, defaults)
