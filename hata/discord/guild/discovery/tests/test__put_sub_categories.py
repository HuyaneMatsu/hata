import vampytest

from ...discovery_category import DiscoveryCategory

from ..fields import put_sub_categories


def _iter_options():
    yield None, False, {'category_ids': []}
    yield None, True, {'category_ids': []}
    yield (DiscoveryCategory.gaming, ), False, {'category_ids': [DiscoveryCategory.gaming.value]}
    yield (DiscoveryCategory.gaming, ), True, {'category_ids': [DiscoveryCategory.gaming.value]}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_sub_categories(input_value, defaults):
    """
    Tests whether ``put_sub_categories`` is working as intended.
    
    Parameters
    ----------
    input_value : `none | tuple<DiscoveryCategory>`
        Value to serialize.
    defaults : `bool`
        Whether fields with their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_sub_categories(input_value, {}, defaults)
