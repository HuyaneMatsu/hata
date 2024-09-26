import vampytest

from ..fields import parse_country_code


def _iter_options():
    yield {}, None
    yield {'country': None}, None
    yield {'country': ''}, None
    yield {'country': 'AA'}, 'AA'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_country_code(input_data):
    """
    Tests whether ``parse_country_code`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    output = parse_country_code(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output
