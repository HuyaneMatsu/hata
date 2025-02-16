import vampytest

from ...embed_field_base import EmbedMediaFlag

from ..fields import put_flags


def _iter_options():
    yield EmbedMediaFlag(0), False, {}
    yield EmbedMediaFlag(0), True, {'flags': 0}
    yield EmbedMediaFlag(1), False, {'flags': 1}
    yield EmbedMediaFlag(1), True, {'flags': 1}


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_flags(input_value, defaults):
    """
    Tests whether ``put_flags`` is working as intended.
    
    Parameters
    ----------
    input_value : ``EmbedMediaFlag``
        The value to serialise.
    defaults : `bool`
        Whether fields of their default value should be included in the output.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_flags(input_value, {}, defaults)
