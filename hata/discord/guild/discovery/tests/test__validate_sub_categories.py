import vampytest

from ...discovery_category import DiscoveryCategory

from ..fields import validate_sub_categories


def _iter_options__passing():
    yield None, None
    yield [], None
    yield [DiscoveryCategory.gaming], (DiscoveryCategory.gaming, )
    yield [DiscoveryCategory.gaming.value], (DiscoveryCategory.gaming, )
    yield [DiscoveryCategory.gaming, DiscoveryCategory.general], (DiscoveryCategory.general, DiscoveryCategory.gaming)


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_sub_categories(input_value):
    """
    Tests whether `validate_sub_categories` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | tuple<DiscoveryCategory>`
    
    Raises
    ------
    TypeError
    """
    return validate_sub_categories(input_value)
