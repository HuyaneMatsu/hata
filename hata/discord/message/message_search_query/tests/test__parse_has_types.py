import vampytest

from ..fields import parse_has_types
from ..preinstanced import MessageSearchHasType


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'has': None,
        },
        None,
    )
    
    yield (
        {
            'has': [],
        },
        None,
    )
    
    yield (
        {
            'has': [
                MessageSearchHasType.embed.value,
                MessageSearchHasType.image.value,
            ],
        },
        (
            MessageSearchHasType.embed,
            MessageSearchHasType.image,
        ),
    )
    
    yield (
        {
            'has': [
                MessageSearchHasType.image.value,
                MessageSearchHasType.embed.value,
            ],
        },
        (
            MessageSearchHasType.embed,
            MessageSearchHasType.image,
        ),
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_has_types(input_data):
    """
    Tests whether ``parse_has_types`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output :  ``None | tuple<MessageSearchHasType>``
    """
    output = parse_has_types(input_data)
    
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, MessageSearchHasType)
    
    return output
