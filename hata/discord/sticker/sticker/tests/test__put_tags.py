import vampytest

from ..fields import put_tags


def test__put_tags():
    """
    Tests whether ``put_tags`` works as intended.
    """
    for input_value, expected_outputs in (
        (None, [{'tags': ''}]),
        (frozenset(('lost', 'emotion')), [{'tags': 'lost, emotion'}, {'tags': 'emotion, lost'}]),
    ):
        output = put_tags(input_value, {}, False)
        vampytest.assert_in(output, expected_outputs)
