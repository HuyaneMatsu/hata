import vampytest

from ..fields import parse_url_large


def _iter_options():
    yield {}, None
    yield {'large_url': None}, None
    yield {'large_url': ''}, None
    yield {'large_url': 'a'}, 'a'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_url_large(input_data):
    """
    Tests whether ``parse_url_large`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    output = parse_url_large(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output
