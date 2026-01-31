import vampytest

from ..fields import put_has_types
from ..preinstanced import MessageSearchHasType


def _iter_options():
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'has': [],
        },
    )
    
    yield (
        (
            MessageSearchHasType.embed,
            MessageSearchHasType.image,
        ),
        False,
        {
            'has': [
                MessageSearchHasType.embed.value,
                MessageSearchHasType.image.value,
            ],
        },
    )
    
    yield (
        (
            MessageSearchHasType.embed,
            MessageSearchHasType.image,
        ),
        True,
        {
            'has': [
                MessageSearchHasType.embed.value,
                MessageSearchHasType.image.value,
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_has_types(input_value, defaults):
    """
    Tests whether ``put_has_types`` is working as intended.
    
    Parameters
    ----------
    input_value : ``None | tuple<MessageSearchHasType>``
        The value to serialise.
    
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_has_types(input_value, {}, defaults)
