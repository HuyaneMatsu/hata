import vampytest

from ....sticker import Sticker

from ..fields import validate_stickers


def test__validate_stickers__0():
    """
    Tests whether ``validate_stickers`` works as intended.
    
    Case: passing.
    """
    sticker_id = 202306140000
    sticker_name = 'Koishi'
    
    sticker = Sticker.precreate(
        sticker_id,
        name = sticker_name,
    )
    
    for input_value, expected_output in (
        (None, {}),
        ([], {}),
        ({}, {}),
        ([sticker], {sticker_id: sticker}),
        ({sticker_id: sticker}, {sticker_id: sticker}),
    ):
        output = validate_stickers(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_stickers__1():
    """
    Tests whether ``validate_stickers`` works as intended.
    
    Case: raising.
    """
    for input_value in (
        12.6,
        [12.6],
        {12.6: 12.6},
    ):
        with vampytest.assert_raises(TypeError):
            validate_stickers(input_value)
