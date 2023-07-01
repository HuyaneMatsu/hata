import vampytest

from ...sticker_pack import StickerPack

from ..fields import validate_pack_id


@vampytest.skip_if(not hasattr(StickerPack, 'precreate'))
def test__validate_pack_id__0():
    """
    Tests whether `validate_pack_id` works as intended.
    
    Case: passing.
    """
    pack_id = 202301040007
    
    for input_value, expected_output in (
        (pack_id, pack_id),
        (str(pack_id), pack_id),
        (StickerPack.precreate(pack_id), pack_id),
    ):
        output = validate_pack_id(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_pack_id__1():
    """
    Tests whether `validate_pack_id` works as intended.
    
    Case: `ValueError`.
    """
    for input_value in (
        '-1',
        -1,
    ):
        with vampytest.assert_raises(AssertionError, ValueError):
            validate_pack_id(input_value)


def test__validate_pack_id__2():
    """
    Tests whether `validate_pack_id` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
    ):
        with vampytest.assert_raises(TypeError):
            validate_pack_id(input_value)
