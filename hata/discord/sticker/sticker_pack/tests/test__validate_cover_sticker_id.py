import vampytest

from ...sticker import Sticker

from ..fields import validate_cover_sticker_id


def test__validate_cover_sticker_id__0():
    """
    Tests whether `validate_cover_sticker_id` works as intended.
    
    Case: passing.
    """
    cover_sticker_id = 202301040010
    
    for input_value, expected_output in (
        (cover_sticker_id, cover_sticker_id),
        (str(cover_sticker_id), cover_sticker_id),
        (Sticker.precreate(cover_sticker_id), cover_sticker_id),
    ):
        output = validate_cover_sticker_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_cover_sticker_id__1():
    """
    Tests whether `validate_cover_sticker_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '-1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_cover_sticker_id(input_value)


def test__validate_cover_sticker_id__2():
    """
    Tests whether `validate_cover_sticker_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_cover_sticker_id(input_value)
