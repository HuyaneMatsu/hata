import vampytest

from ....embed import Embed

from ..fields import parse_embeds


def test__parse_embeds():
    """
    Tests whether ``parse_embeds`` works as intended.
    """
    embed_0 = Embed('Hell')
    embed_1 = Embed('Rose')
    
    for input_value, expected_output in (
        ({}, None),
        ({'embeds': None}, None),
        ({'embeds': [embed_0.to_data()]}, (embed_0, )),
        ({'embeds': [embed_0.to_data(), embed_1.to_data()]}, (embed_0, embed_1)),
    ):
        output = parse_embeds(input_value)
        vampytest.assert_eq(output, expected_output)
