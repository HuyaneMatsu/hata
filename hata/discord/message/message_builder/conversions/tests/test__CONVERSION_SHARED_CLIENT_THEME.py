import vampytest

from ....shared_client_theme import SharedClientTheme

from ..shared_client_theme import CONVERSION_SHARED_CLIENT_THEME


def _iter_options__set_validator():
    shared_client_theme = SharedClientTheme(intensity = 6)
    
    yield object(), []
    yield None, [None]
    yield shared_client_theme, [shared_client_theme]


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_SHARED_CLIENT_THEME__set_validator(input_value):
    """
    Tests whether ``CONVERSION_SHARED_CLIENT_THEME.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : ``list<None | SharedClientTheme>``
    """
    return [*CONVERSION_SHARED_CLIENT_THEME.set_validator(input_value)]


def _iter_options__serializer_optional():
    shared_client_theme = SharedClientTheme(intensity = 6)
    
    yield None, []
    yield shared_client_theme, [shared_client_theme.to_data()]


@vampytest._(vampytest.call_from(_iter_options__serializer_optional()).returning_last())
def test__CONVERSION_SHARED_CLIENT_THEME__serializer_optional(input_value):
    """
    Tests whether ``CONVERSION_SHARED_CLIENT_THEME.serializer_optional`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | SharedClientTheme``
        Value to test.
    
    Returns
    -------
    output : ``list<SharedClientTheme>``
    """
    return [*CONVERSION_SHARED_CLIENT_THEME.serializer_optional(input_value)]


def _iter_options__serializer_required():
    shared_client_theme = SharedClientTheme(intensity = 6)
    
    yield None, None
    yield shared_client_theme, shared_client_theme.to_data()


@vampytest._(vampytest.call_from(_iter_options__serializer_required()).returning_last())
def test__CONVERSION_SHARED_CLIENT_THEME__serializer_required(input_value):
    """
    Tests whether ``CONVERSION_SHARED_CLIENT_THEME.serializer_required`` works as intended.
    
    Parameters
    ----------
    input_value : ``None | SharedClientTheme``
        Value to test.
    
    Returns
    -------
    output : ``SharedClientTheme``
    """
    return CONVERSION_SHARED_CLIENT_THEME.serializer_required(input_value)
