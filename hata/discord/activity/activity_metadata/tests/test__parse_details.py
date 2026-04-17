import vampytest

from ..fields import parse_details


def _iter_options():
    yield {}, None
    yield {'details': None}, None
    yield {'details': ''}, None
    yield {'details': 'a'}, 'a'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_details(input_data):
    """
    Tests whether ``parse_details`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    output = parse_details(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output
