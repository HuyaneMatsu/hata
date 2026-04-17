import vampytest

from ..fields import validate_default_forum_layout
from ..preinstanced import ForumLayout


def _iter_options__passing():
    yield None, ForumLayout.none
    yield ForumLayout.list, ForumLayout.list
    yield ForumLayout.list.value, ForumLayout.list


def _iter_options__type_error():
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_default_forum_layout(input_value):
    """
    Validates whether ``validate_default_forum_layout`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``ForumLayout``
    
    Raises
    ------
    TypeError
    """
    output = validate_default_forum_layout(input_value)
    vampytest.assert_instance(output, ForumLayout)
    return output
