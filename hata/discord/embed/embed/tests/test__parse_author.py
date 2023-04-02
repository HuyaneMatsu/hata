import vampytest

from ...embed_author import EmbedAuthor

from ..fields import parse_author


def test__parse_author():
    """
    Tests whether ``parse_author`` works as intended.
    """
    author = EmbedAuthor(name = 'hell')
    
    for input_data, expected_output in (
        ({}, None),
        ({'author': None}, None),
        ({'author': author.to_data()}, author),
    ):
        output = parse_author(input_data)
        vampytest.assert_eq(output, expected_output)
