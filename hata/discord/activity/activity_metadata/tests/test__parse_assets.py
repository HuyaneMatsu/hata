import vampytest

from ...activity_assets import ActivityAssets

from ..fields import parse_assets


def _iter_options():
    assets = ActivityAssets(image_large = 'hell')
    
    yield ({}, None)
    yield ({'assets': None}, None)
    yield ({'assets': assets.to_data()}, assets)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_assets(input_data):
    """
    Tests whether ``parse_assets`` works as intended.
    
    Parameters
    ----------
    input_data : dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | ActivityAssets`
    """
    output = parse_assets(input_data)
    vampytest.assert_instance(output, ActivityAssets, nullable = True)
    return output
