import vampytest

from ...shared_client_theme import SharedClientTheme

from ..fields import parse_shared_client_theme


def _iter_options():
    shared_client_theme = SharedClientTheme(
        intensity = 6,
    )
    
    yield (
        {},
        None,
    )
    
    yield (
        {
            'shared_client_theme': None,
        },
        None,
    )
    
    yield (
        {
            'shared_client_theme': shared_client_theme.to_data(),
        },
        shared_client_theme,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_shared_client_theme(input_data):
    """
    Tests whether ``parse_shared_client_theme`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : ``None | SharedClientTheme``
    """
    output = parse_shared_client_theme(input_data)
    vampytest.assert_instance(output, SharedClientTheme, nullable = True)
    return output
