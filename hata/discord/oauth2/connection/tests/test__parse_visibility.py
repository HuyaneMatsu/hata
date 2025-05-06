import vampytest

from ..preinstanced import ConnectionVisibility

from ..fields import parse_visibility


def _iter_options():
    yield (
        {},
        ConnectionVisibility.user_only,
    )
    
    yield (
        {
            'visibility': None,
        },
        ConnectionVisibility.user_only,
    )
    
    yield (
        {
            'visibility': ConnectionVisibility.user_only.value,
        },
        ConnectionVisibility.user_only,
    )
    
    yield (
        {
            'visibility': ConnectionVisibility.everyone.value,
        },
        ConnectionVisibility.everyone,
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_visibility(input_data):
    """
    Tests whether ``parse_visibility`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``ConnectionVisibility``
    """
    output = parse_visibility(input_data)
    vampytest.assert_instance(output, ConnectionVisibility)
    return output
