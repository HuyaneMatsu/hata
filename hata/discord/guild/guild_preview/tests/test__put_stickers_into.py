import vampytest

from ....sticker import Sticker

from ..fields import put_stickers_into


def test__put_stickers_into():
    """
    Tests whether ``put_stickers_into`` works as intended.
    """
    sticker_0 = Sticker.precreate(202301080010, name = 'rose')
    
    for input_value, expected_output in (
        (
            {},
            {'stickers': []},
        ), (
            {sticker_0.id: sticker_0},
            {'stickers': [sticker_0.to_data(defaults = True, include_internals = True)]},
        ),
    ):
        output = put_stickers_into(input_value, {}, True)
        vampytest.assert_eq(output, expected_output)
