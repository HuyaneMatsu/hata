import vampytest

from ..fields import parse_author_types
from ..preinstanced import MessageSearchAuthorType


def _iter_options():
    yield (
        {},
        None,
    )
    
    yield (
        {
            'author_type': None,
        },
        None,
    )
    
    yield (
        {
            'author_type': [],
        },
        None,
    )
    
    yield (
        {
            'author_type': [
                MessageSearchAuthorType.bot.value,
                MessageSearchAuthorType.user.value,
            ],
        },
        (
            MessageSearchAuthorType.bot,
            MessageSearchAuthorType.user,
        ),
    )
    
    yield (
        {
            'author_type': [
                MessageSearchAuthorType.user.value,
                MessageSearchAuthorType.bot.value,
            ],
        },
        (
            MessageSearchAuthorType.bot,
            MessageSearchAuthorType.user,
        ),
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_author_types(input_data):
    """
    Tests whether ``parse_author_types`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output :  ``None | tuple<MessageSearchAuthorType>``
    """
    output = parse_author_types(input_data)
    
    vampytest.assert_instance(output, tuple, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, MessageSearchAuthorType)
    
    return output
