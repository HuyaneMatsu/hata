import vampytest

from ..utils import escape_markdown


def iter_options():
    yield None, None
    yield '', ''
    yield 'aya', 'aya'
    yield 'aya_aya', 'aya\\_aya'
    yield '\\', '\\\\'
    yield '_', '\\_'
    yield '*', '\\*'
    yield '|', '\\|'
    yield '~', '\\~'
    yield '>', '\\>'
    yield ':', '\\:'
    yield '[', '\\['
    yield ']', '\\]'
    yield '#', '\\#'
    yield '-', '\\-'
    yield '`', '\\`'


@vampytest._(vampytest.call_from(iter_options()).returning_last())
def test__escape_markdown(input_value):
    """
    Tests whether ``escape_markdown`` works as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        Input value
    
    Returns
    -------
    output : `None | str`
    """
    output = escape_markdown(input_value)
    vampytest.assert_instance(output, str, nullable = True)
    return output
