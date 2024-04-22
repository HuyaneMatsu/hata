import vampytest

from ..fields import put_layout_into
from ..preinstanced import PollLayout


def _iter_options():
    yield PollLayout.none, False, {'layout_type': PollLayout.none.value}
    yield PollLayout.none, True, {'layout_type': PollLayout.none.value}
    yield PollLayout.default, False, {}
    yield PollLayout.default, True, {'layout_type': PollLayout.default.value}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_layout_into(input_value, defaults):
    """
    Tests whether ``put_layout_into`` is working as intended.
    
    Parameters
    ----------
    input_value : ``PollLayout``
        Value to serialize.
    defaults : `bool`
        Whether fields with their default value should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_layout_into(input_value, {}, defaults)
