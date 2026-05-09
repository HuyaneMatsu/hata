import vampytest

from ....color import Color

from ..name_style import NameStyle
from ..preinstanced import NameStyleEffect, NameStyleFont

from .test__NameStyle__constructor import _assert_fields_set


def test__NameStyle__copy():
    """
    Tests whether ``NameStyle.copy`` works as intended.
    """
    colors = [Color(123), Color(125)]
    effect = NameStyleEffect.pop
    font = NameStyleFont.modern
    
    name_style = NameStyle(
        colors = colors,
        effect = effect,
        font = font,
    )
    copy = name_style.copy()
    
    _assert_fields_set(copy)
    vampytest.assert_not_is(name_style, copy)
    vampytest.assert_eq(name_style, copy)


def test__NameStyle__copy_with__no_fields():
    """
    Tests whether ``NameStyle.copy_with`` works as intended.
    
    Case: No fields given.
    """
    colors = [Color(123), Color(125)]
    effect = NameStyleEffect.pop
    font = NameStyleFont.modern
    
    name_style = NameStyle(
        colors = colors,
        effect = effect,
        font = font,
    )
    copy = name_style.copy_with()
    
    _assert_fields_set(copy)
    vampytest.assert_not_is(name_style, copy)
    vampytest.assert_eq(name_style, copy)


def test__NameStyle__copy_with__all_fields():
    """
    Tests whether ``NameStyle.copy_with`` works as intended.
    
    Case: All fields given.
    """
    old_colors = [Color(123), Color(125)]
    old_effect = NameStyleEffect.pop
    old_font = NameStyleFont.modern
    
    new_colors = [Color(123), Color(127)]
    new_effect = NameStyleEffect.neon
    new_font = NameStyleFont.sakura
    
    name_style = NameStyle(
        colors = old_colors,
        effect = old_effect,
        font = old_font,
    )
    copy = name_style.copy_with(
        colors = new_colors,
        effect = new_effect,
        font = new_font,
    )
    
    _assert_fields_set(copy)
    vampytest.assert_not_is(name_style, copy)

    vampytest.assert_eq(copy.colors, tuple(new_colors))
    vampytest.assert_eq(copy.effect, new_effect)
    vampytest.assert_is(copy.font, new_font)
