import vampytest

from ...media_info import MediaInfo

from ..fields import validate_media


def _iter_options__passing():
    media = MediaInfo.precreate(
        height = 55,
        proxy_url = 'https://orindance.party/proxy',
        url = 'https://orindance.party',
        width = 56,
    )
    
    yield media, media
    
    url = 'https://orindance.party'
    
    yield url, MediaInfo(url)


def _iter_options__type_error():
    yield None
    yield 12.6


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
def test__validate_media(input_value):
    """
    Tests whether `validate_media` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to validate.
    
    Returns
    -------
    output : ``MediaInfo``
    
    Raises
    ------
    TypeError
    """
    output = validate_media(input_value)
    vampytest.assert_instance(output, MediaInfo)
    return output
