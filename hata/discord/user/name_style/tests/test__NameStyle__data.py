import vampytest

from ....color import Color

from ..name_style import NameStyle
from ..preinstanced import NameStyleEffect, NameStyleFont

from .test__NameStyle__constructor import _assert_fields_set


def test__NameStyle__from_data():
    """
    Tests whether ``NameStyle.from_data`` works as intended.
    """
    colors = [Color(123), Color(125)]
    effect = NameStyleEffect.pop
    font = NameStyleFont.modern
    
    data = {
        'colors': [int(color) for color in colors],
        'effect_id': effect.value,
        'font_id': font.value,
    }
    
    name_style = NameStyle.from_data(data)
    _assert_fields_set(name_style)
    
    vampytest.assert_eq(name_style.colors, tuple(colors))
    vampytest.assert_eq(name_style.effect, effect)
    vampytest.assert_is(name_style.font, font)


def test__NameStyle__to_data():
    """
    Tests whether ``NameStyle.to_data`` works as intended.
    
    Case: Include defaults.
    """
    colors = [Color(123), Color(125)]
    effect = NameStyleEffect.pop
    font = NameStyleFont.modern
    
    name_style = NameStyle(
        colors = colors,
        effect = effect,
        font = font,
    )
    
    expected_output = {
        'colors': [int(color) for color in colors],
        'effect_id': effect.value,
        'font_id': font.value,
    }
    
    vampytest.assert_eq(
        name_style.to_data(
            defaults = True,
        ),
        expected_output,
    )
