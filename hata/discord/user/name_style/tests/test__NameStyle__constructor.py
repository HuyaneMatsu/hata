import vampytest

from ....color import Color

from ..name_style import NameStyle
from ..preinstanced import NameStyleEffect, NameStyleFont


def _assert_fields_set(name_style):
    """
    Asserts whether all fields of the given  plate are set.
    
    Parameters
    ----------
    name_style : ``NameStyle``
    """
    vampytest.assert_instance(name_style, NameStyle)
    vampytest.assert_instance(name_style.colors, tuple, nullable = True)
    vampytest.assert_instance(name_style.effect, NameStyleEffect)
    vampytest.assert_instance(name_style.font, NameStyleFont)


def test__NameStyle__new__no_fields():
    """
    Tests whether ``NameStyle.__new__`` works as intended.
    
    Case: No parameters.
    """
    name_style = NameStyle()
    _assert_fields_set(name_style)


def test__NameStyle__new__all_fields():
    """
    Tests whether ``NameStyle.__new__`` works as intended.
    
    Case: all fields.
    """
    colors = [Color(123), Color(125)]
    effect = NameStyleEffect.pop
    font = NameStyleFont.modern
    
    name_style = NameStyle(
        colors = colors,
        effect = effect,
        font = font,
    )
    _assert_fields_set(name_style)
    
    vampytest.assert_eq(name_style.colors, tuple(colors))
    vampytest.assert_eq(name_style.effect, effect)
    vampytest.assert_is(name_style.font, font)
