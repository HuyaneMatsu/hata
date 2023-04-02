import vampytest

from ...embed_footer import EmbedFooter

from ..fields import parse_footer


def test__parse_footer():
    """
    Tests whether ``parse_footer`` works as intended.
    """
    footer = EmbedFooter(text = 'hell')
    
    for input_data, expected_output in (
        ({}, None),
        ({'footer': None}, None),
        ({'footer': footer.to_data()}, footer),
    ):
        output = parse_footer(input_data)
        vampytest.assert_eq(output, expected_output)
