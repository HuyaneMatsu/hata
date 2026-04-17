import vampytest

from ..preinstanced import AnsiBackgroundColor, AnsiForegroundColor, AnsiTextDecoration
from ..utils import create_ansi_format_code


def _iter_options():
    yield (
        {},
        '\x1b[0m',
    )
    
    yield (
        {
            'text_decoration': AnsiTextDecoration.bold,
        },
        '\u001b[1m'
    )
    
    yield (
        {
            'background_color': AnsiBackgroundColor.gray,
        },
        '\u001b[44m'
    )
    
    yield (
        {
            'foreground_color': AnsiForegroundColor.red,
        },
        '\u001b[31m'
    )
    
    yield (
        {
            'text_decoration': AnsiTextDecoration.bold,
            'background_color': AnsiBackgroundColor.gray,
            'foreground_color': AnsiForegroundColor.red,
        },
        '\u001b[1;44;31m'
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__create_ansi_format_code(keyword_parameters):
    """
    tests whether ``create_ansi_format_code`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to call ``create_ansi_format_code`` with.
    
    Returns
    -------
    output : `str`
    """
    output = create_ansi_format_code(**keyword_parameters)
    vampytest.assert_instance(output, str)
    return output
