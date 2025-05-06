import vampytest

from ..preinstanced import ConnectionVisibility

from ..fields import put_visibility


def _iter_options():
    yield (
        ConnectionVisibility.user_only,
        False,
        {},
    )
    
    yield (
        ConnectionVisibility.user_only,
        True,
        {
            'visibility': ConnectionVisibility.user_only.value,
        },
    )
    
    yield (
        ConnectionVisibility.everyone,
        False,
        {
            'visibility': ConnectionVisibility.everyone.value,
        },
    )
    
    yield (
        ConnectionVisibility.everyone,
        True,
        {
            'visibility': ConnectionVisibility.everyone.value,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_visibility(input_value, defaults):
    """
    Tests whether ``put_visibility`` is working as intended.
    
    Parameters
    ----------
    input_value : ``ConnectionVisibility``
        The value to serialize.
    
    defaults : `bool`
        Whether values with their default should be serialized as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_visibility(input_value, {}, defaults)
