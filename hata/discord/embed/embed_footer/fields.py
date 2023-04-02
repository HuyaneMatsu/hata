__all__ = ()

from ...field_parsers import nullable_string_parser_factory
from ...field_putters import nullable_string_putter_factory, url_optional_putter_factory
from ...field_validators import nullable_string_validator_factory, url_optional_validator_factory

from .constants import EMBED_FOOTER_TEXT_LENGTH_MAX

# icon_url

parse_icon_url = nullable_string_parser_factory('icon_url')
put_icon_url_into = url_optional_putter_factory('icon_url')
# url validator doesnt allow attachment:\\image.png formats
validate_icon_url = nullable_string_validator_factory('icon_url', 0, 16384)

# icon_proxy_url

parse_icon_proxy_url = nullable_string_parser_factory('proxy_icon_url')
put_icon_proxy_url_into = url_optional_putter_factory('proxy_icon_url')
validate_icon_proxy_url = url_optional_validator_factory('icon_proxy_url')

# text

parse_text = nullable_string_parser_factory('text')
put_text_into = nullable_string_putter_factory('text')


def validate_text(text):
    """
    Validates the given embed footer text.
    
    Parameters
    ----------
    text : `None`, `str`, `object`
        Embed footer text.
    
    Returns
    -------
    text : `None`, `str`
    
    Raises
    ------
    TypeError
        - If `text`'s type is incorrect.
    ValueError
        - If `text`'s length is out of the expected range.
    """
    if text is None:
        return None
    
    if not isinstance(text, str):
        text = str(text)
    
    text_length = len(text)
    if text_length == 0:
        return None
    
    if text_length > EMBED_FOOTER_TEXT_LENGTH_MAX:
        raise ValueError(
            f'`text` length` must be <= {EMBED_FOOTER_TEXT_LENGTH_MAX}, got {text_length}; text = {text!r}.'
        )
    
    return text
