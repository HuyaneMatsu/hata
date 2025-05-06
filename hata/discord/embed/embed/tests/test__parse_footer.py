import vampytest

from ...embed_footer import EmbedFooter

from ..fields import parse_footer


def _iter_options():
    footer = EmbedFooter(text = 'hell')
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'footer': None,
        },
        None,
    )
    
    yield (
        {
            'footer': footer.to_data(),
        },
        footer,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_footer(input_data):
    """
    Tests whether ``parse_footer`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | EmbedFooter``
    """
    output = parse_footer(input_data)
    vampytest.assert_instance(output, EmbedFooter, nullable = True)
    return output
