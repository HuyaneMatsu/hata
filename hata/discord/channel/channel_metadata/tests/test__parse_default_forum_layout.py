import vampytest

from ..preinstanced import ForumLayout

from ..fields import parse_default_forum_layout


def _iter_options():
    yield {}, ForumLayout.none
    yield {'default_forum_layout': None}, ForumLayout.none
    yield {'default_forum_layout': ForumLayout.list.value}, ForumLayout.list
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_default_forum_layout(input_data):
    """
    Tests whether ``parse_default_forum_layout`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``ForumLayout``
    """
    output = parse_default_forum_layout(input_data)
    vampytest.assert_instance(output, ForumLayout)
    return output
