import vampytest

from ...embed_footer import EmbedFooter

from ..fields import put_footer


def _iter_options():
    footer = EmbedFooter(text = 'hell')
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'footer': None,
        },
    )
    
    yield (
        footer,
        False,
        {
            'footer': footer.to_data(),
        },
    )
    
    yield (
        footer,
        True,
        {
            'footer': footer.to_data(defaults = True),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_footer(input_value, defaults):
    """
    Tests whether ``put_footer`` is working as intended.
    
    Parameters
    ----------
    input_value : ``None | EmbedFooter``
        The value to serialize.
    
    defaults : `bool`
        Whether fields with as their default should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_footer(input_value, {}, defaults)
