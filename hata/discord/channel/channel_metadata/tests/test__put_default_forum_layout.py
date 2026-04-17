import vampytest

from ..fields import put_default_forum_layout
from ..preinstanced import ForumLayout


def _iter_options():
    yield ForumLayout.none, False, {}
    yield ForumLayout.none, True, {'default_forum_layout': ForumLayout.none.value}
    yield ForumLayout.list, False, {'default_forum_layout': ForumLayout.list.value}
    yield ForumLayout.list, True, {'default_forum_layout': ForumLayout.list.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_default_forum_layout(input_value, defaults):
    """
    Tests whether ``put_default_forum_layout`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ForumLayout``
        Value to serialize.
    defaults : `bool`
        Whether fields with their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_default_forum_layout(input_value, {}, defaults)
