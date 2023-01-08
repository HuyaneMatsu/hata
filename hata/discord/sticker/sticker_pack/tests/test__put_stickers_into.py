import vampytest

from ...sticker import Sticker

from ..fields import put_stickers_into


@vampytest.skip_if(not hasattr(Sticker, 'to_data'))
def test__put_stickers_into():
    """
    Tests whether ``put_stickers_into`` works as intended.
    """
    sticker_0 = Sticker.precreate(202301050016, name = 'just')
    sticker_1 = Sticker.precreate(202301050017, name = 'flowering')
    
    for input_value, defaults, expected_output,  in (
        (
            None,
            False,
            {'stickers': []},
        ), (
            None,
            True,
            {'stickers': []},
        ), (
            frozenset((sticker_0, sticker_1)),
            False,
            {'stickers': [sticker_0.to_data(include_internals = True), sticker_1.to_data(include_internals = True)]},
        ), (
            frozenset((sticker_0, sticker_1)),
            True,
            {
                'stickers': [
                    sticker_0.to_data(defaults = True, include_internals = True),
                    sticker_1.to_data(defaults = True, include_internals = True),
                ],
            },
        ),
    ):
        output = put_stickers_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
