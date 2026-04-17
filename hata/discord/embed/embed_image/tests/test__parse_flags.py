import vampytest

from ...embed_field_base import EmbedMediaFlag

from ..fields import parse_flags


def _iter_options():
    yield {}, EmbedMediaFlag(0)
    yield {'flags': 1}, EmbedMediaFlag(1)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_flags(input_data):
    """
    Tests whether ``parse_flags`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse the flags from.
    
    Returns
    -------
    output : ``EmbedMediaFlag``
    """
    output = parse_flags(input_data)
    vampytest.assert_instance(output, EmbedMediaFlag)
    return output
