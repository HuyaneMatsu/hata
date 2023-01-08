import vampytest

from ...sticker import Sticker

from ..fields import parse_stickers


@vampytest.skip_if(not hasattr(Sticker, 'to_data'))
def test__parse_stickers():
    """
    Tests whether ``parse_stickers`` works as intended.
    """
    sticker_0 = Sticker.precreate(202301050014, name = 'just')
    sticker_1 = Sticker.precreate(202301050015, name = 'flowering')
    
    for input_data, expected_output in (
        (
            {},
            None,
        ), (
            {'stickers': None},
            None,
        ), (
            {'stickers': []},
            None,
        ), (
            {'stickers': [sticker_0.to_data(include_internals = True), sticker_1.to_data(include_internals = True)]},
            frozenset((sticker_0, sticker_1)),
        ),
    ):
        output = parse_stickers(input_data)
        vampytest.assert_eq(output, expected_output)
