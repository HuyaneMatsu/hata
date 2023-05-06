import vampytest

from ....embed import Embed

from ..fields import put_embeds_into


def test__put_embeds_into():
    """
    Tests whether ``put_embeds_into`` works as intended.
    """
    embed_0 = Embed('Hell')
    embed_1 = Embed('Rose')
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'embeds': []}),
        ((embed_0, ), False, {'embeds': [embed_0.to_data()]},),
        (
            (embed_0, embed_1),
            True,
            {'embeds': [embed_0.to_data(defaults = True), embed_1.to_data(defaults = True)]},
        ),
    ):
        output = put_embeds_into(input_value, {}, defaults)
        vampytest.assert_eq(output, expected_output)
