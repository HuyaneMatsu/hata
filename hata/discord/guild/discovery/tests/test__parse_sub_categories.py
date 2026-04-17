import vampytest

from ...discovery_category import DiscoveryCategory

from ..fields import parse_sub_categories


def _iter_options():
    yield {}, None
    yield {'category_ids': None}, None
    yield {'category_ids': []}, None
    yield {'category_ids': [DiscoveryCategory.gaming.value]}, (DiscoveryCategory.gaming,)
    yield (
        {'category_ids': [DiscoveryCategory.gaming.value, DiscoveryCategory.general.value]},
        (DiscoveryCategory.general, DiscoveryCategory.gaming,),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_sub_categories(input_data):
    """
    Tests whether ``parse_sub_categories`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | tuple<DiscoveryCategory>`
    """
    return parse_sub_categories(input_data)
