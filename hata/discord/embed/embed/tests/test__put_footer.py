import vampytest

from ...embed_footer import EmbedFooter

from ..fields import put_footer


def test__put_footer():
    """
    Tests whether ``put_footer`` is working as intended.
    """
    footer = EmbedFooter(text = 'hell')
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (footer, False, {'footer': footer.to_data()}),
        (footer, True, {'footer': footer.to_data(defaults = True)}),
    ):
        data = put_footer(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
