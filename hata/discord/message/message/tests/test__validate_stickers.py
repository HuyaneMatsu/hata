import vampytest

from ....sticker import Sticker

from ..fields import validate_stickers


def test__validate_stickers__0():
    """
    Tests whether ``validate_stickers`` works as intended.
    
    Case: Passing.
    """
    sticker_0 = Sticker.precreate(202305010012, name = 'Orin')
    sticker_1 = Sticker.precreate(202305010013, name = 'Okuu')
    
    for input_value, expected_output in (
        (
            None,
            None,
        ), (
            [],
            None,
        ), (
            [sticker_0],
            (sticker_0,),
        ), (
            [sticker_0, sticker_1],
            (sticker_0, sticker_1),
        ),
    ):
        output = validate_stickers(input_value)
        vampytest.assert_eq(output, expected_output)



def test__validate_stickers__1():
    """
    Tests whether ``validate_stickers`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
        [12.6],
    ):
        with vampytest.assert_raises(TypeError):
            validate_stickers(input_value)
