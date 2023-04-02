import vampytest

from ...embed_author import EmbedAuthor

from ..fields import put_author_into


def test__put_author_into():
    """
    Tests whether ``put_author_into`` is working as intended.
    """
    author = EmbedAuthor(name = 'hell')
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (author, False, {'author': author.to_data()}),
        (author, True, {'author': author.to_data(defaults = True)}),
    ):
        data = put_author_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
