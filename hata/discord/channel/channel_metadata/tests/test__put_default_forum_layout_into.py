import vampytest

from ..fields import put_default_forum_layout_into
from ..preinstanced import ForumLayout


def test__put_default_forum_layout_into():
    """
    Tests whether ``put_default_forum_layout_into`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (ForumLayout.none, False, {}),
        (ForumLayout.none, True, {'default_forum_layout': ForumLayout.none.value}),
        (ForumLayout.list, False, {'default_forum_layout': ForumLayout.list.value}),
    ):
        data = put_default_forum_layout_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
