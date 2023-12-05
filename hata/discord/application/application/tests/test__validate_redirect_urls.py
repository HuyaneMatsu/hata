import vampytest

from ..fields import validate_redirect_urls


def _iter_options__passing():
    url_0 = 'https://orindance.party/'
    url_1 = 'https://www.astil.dev/project/hata/'
    
    yield None, None
    yield [], None
    yield url_0, (url_0, )
    yield [url_0], (url_0, )
    yield [url_1, url_0], (url_0, url_1)


def _iter_options__type_error():
    yield 12.6
    yield [12.6]


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_redirect_urls(input_value):
    """
    Tests whether `validate_redirect_urls` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : `None | tuple<str>`
    
    Raises
    ------
    TypeError
    """
    return validate_redirect_urls(input_value)
