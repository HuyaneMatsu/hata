import vampytest

from ...shared_client_theme import SharedClientTheme

from ..fields import put_shared_client_theme


def _iter_options():
    shared_client_theme = SharedClientTheme(
        intensity = 5,
    )
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {
            'shared_client_theme': None,
        },
    )
    
    yield (
        shared_client_theme,
        False,
        {
            'shared_client_theme': shared_client_theme.to_data(defaults = False),
        },
    )
    
    yield (
        shared_client_theme,
        True,
        {
            'shared_client_theme': shared_client_theme.to_data(defaults = True),
        },
    )

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_shared_client_theme(input_value, defaults):
    """
    Tests whether ``put_shared_client_theme`` is working as intended.
    
    Parameters
    ----------
    input_value : ``None | SharedClientTheme``
        The value to serialize.
    
    defaults : `bool`
        Whether values as their default should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_shared_client_theme(input_value, {}, defaults)
