import vampytest

from ....color import Color

from ..name_style import NameStyle
from ..preinstanced import NameStyleEffect, NameStyleFont


def test__NameStyle__repr():
    """
    Tests whether ``NameStyle.__repr__`` works as intended.
    """
    colors = [Color(123), Color(125)]
    effect = NameStyleEffect.pop
    font = NameStyleFont.modern
    
    name_style = NameStyle(
        colors = colors,
        effect = effect,
        font = font,
    )
    
    output = repr(name_style)
    vampytest.assert_instance(output, str)


def test__NameStyle__hash():
    """
    Tests whether ``NameStyle.__hash__`` works as intended.
    """
    colors = [Color(123), Color(125)]
    effect = NameStyleEffect.pop
    font = NameStyleFont.modern
    
    name_style = NameStyle(
        colors = colors,
        effect = effect,
        font = font,
    )
    
    output = hash(name_style)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    colors = [Color(123), Color(125)]
    effect = NameStyleEffect.pop
    font = NameStyleFont.modern
    
    keyword_parameters = {
        'colors': colors,
        'effect': effect,
        'font': font,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'colors': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'effect': NameStyleEffect.neon,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'font': NameStyleFont.sakura,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__NameStyle__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``NameStyle.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    name_style_0 = NameStyle(**keyword_parameters_0)
    name_style_1 = NameStyle(**keyword_parameters_1)
    
    output = name_style_0 == name_style_1
    vampytest.assert_instance(output, bool)
    return output
