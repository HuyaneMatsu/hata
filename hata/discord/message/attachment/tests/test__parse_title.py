import vampytest

from ..fields import parse_title


def _iter_options():
    yield {}, None
    yield {'title': None}, None
    yield {'title': ''}, None
    yield {'title': 'a'}, 'a'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_title(input_data):
    """
    Tests whether ``parse_title`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    output = parse_title(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output
