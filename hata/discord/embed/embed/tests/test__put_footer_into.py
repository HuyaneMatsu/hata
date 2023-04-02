import vampytest

from ...embed_footer import EmbedFooter

from ..fields import put_footer_into


def test__put_footer_into():
    """
    Tests whether ``put_footer_into`` is working as intended.
    """
    footer = EmbedFooter(text = 'hell')
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (footer, False, {'footer': footer.to_data()}),
        (footer, True, {'footer': footer.to_data(defaults = True)}),
    ):
        data = put_footer_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
