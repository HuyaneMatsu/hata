import vampytest

from ..fields import put_tags_into


def test__put_tags_into():
    """
    Tests whether ``put_tags_into`` works as intended.
    """
    for input_value, expected_outputs in (
        (None, [{'tags': ''}]),
        (frozenset(('lost', 'emotion')), [{'tags': 'lost, emotion'}, {'tags': 'emotion, lost'}]),
    ):
        output = put_tags_into(input_value, {}, False)
        vampytest.assert_in(output, expected_outputs)
