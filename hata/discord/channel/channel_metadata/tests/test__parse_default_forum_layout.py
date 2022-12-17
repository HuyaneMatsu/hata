import vampytest

from ..preinstanced import ForumLayout

from ..fields import parse_default_forum_layout


def test__parse_default_forum_layout():
    """
    Tests whether ``parse_default_forum_layout`` works as intended.
    """
    for input_data, expected_output in (
        ({}, ForumLayout.none),
        ({'default_forum_layout': None}, ForumLayout.none),
        ({'default_forum_layout': ForumLayout.list.value}, ForumLayout.list),
    ):
        output = parse_default_forum_layout(input_data)
        vampytest.assert_is(output, expected_output)
