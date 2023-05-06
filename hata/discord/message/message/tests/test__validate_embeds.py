import vampytest

from ....embed import Embed

from ..fields import validate_embeds


def test__validate_embeds__0():
    """
    Tests whether ``validate_embeds`` works as intended.
    
    Case: passing.
    """
    embed_0 = Embed('Hell')
    embed_1 = Embed('Rose')
    
    for input_value, expected_output in (
        (None, None),
        ([], None),
        ([embed_0], (embed_0, )),
        ([embed_0, embed_1], (embed_0, embed_1)),
    ):
        output = validate_embeds(input_value)
        vampytest.assert_eq(output, expected_output)


def test__validate_embeds__1():
    """
    Tests whether ``validate_embeds`` works as intended.
    
    Case: `TypeError`.
    """
    for input_value in (
        12.6,
        [12.6],
    ):
        with vampytest.assert_raises(TypeError):
            validate_embeds(input_value)
