import vampytest

from ...embed_author import EmbedAuthor

from ..fields import put_author


def test__put_author():
    """
    Tests whether ``put_author`` is working as intended.
    """
    author = EmbedAuthor(name = 'hell')
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (author, False, {'author': author.to_data()}),
        (author, True, {'author': author.to_data(defaults = True)}),
    ):
        data = put_author(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
