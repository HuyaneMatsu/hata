import vampytest

from ..fields import put_author_types
from ..preinstanced import MessageSearchAuthorType


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
            'author_type': [],
        },
    )
    
    yield (
        (
            MessageSearchAuthorType.bot,
            MessageSearchAuthorType.user,
        ),
        False,
        {
            'author_type': [
                MessageSearchAuthorType.bot.value,
                MessageSearchAuthorType.user.value,
            ],
        },
    )
    
    yield (
        (
            MessageSearchAuthorType.bot,
            MessageSearchAuthorType.user,
        ),
        True,
        {
            'author_type': [
                MessageSearchAuthorType.bot.value,
                MessageSearchAuthorType.user.value,
            ],
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_author_types(input_value, defaults):
    """
    Tests whether ``put_author_types`` is working as intended.
    
    Parameters
    ----------
    input_value : ``None | tuple<MessageSearchAuthorType>``
        The value to serialise.
    
    defaults : `bool`
        Whether values with their default value should be included in the output as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_author_types(input_value, {}, defaults)
