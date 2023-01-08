import vampytest

from ....sticker import Sticker

from ..fields import parse_stickers


def test__parse_stickers():
    """
    Tests whether ``parse_stickers`` works as intended.
    """
    sticker_0 = Sticker.precreate(202301080008, name = 'rose')
    sticker_1 = Sticker.precreate(202301080009, name = 'slayer')
    
    for input_data, input_entities, expected_output in (
        (
            {},
            {},
            {},
        ), (
            {'stickers': None},
            {},
            {},
        ), (
            {'stickers': []},
            {},
            {},
        ), (
            {'stickers': [sticker_0.to_data(defaults = True, include_internals = True)]},
            {},
            {sticker_0.id: sticker_0},
        ), (
            {'stickers': [sticker_1.to_data(defaults = True, include_internals = True)]},
            {sticker_0.id: sticker_0},
            {sticker_1.id: sticker_1},
        ),
    ):
        output = parse_stickers(input_data, input_entities)
        vampytest.assert_eq(output, expected_output)
