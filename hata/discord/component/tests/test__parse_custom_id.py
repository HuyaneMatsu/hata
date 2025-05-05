import vampytest

from ..shared_fields import parse_custom_id


def _iter_options():
    yield {}, None
    yield {'custom_id': None}, None
    yield {'custom_id': ''}, None
    yield {'custom_id': 'a'}, 'a'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_custom_id(input_data):
    """
    Tests whether ``parse_custom_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | str`
    """
    output = parse_custom_id(input_data)
    vampytest.assert_instance(output, str, nullable = True)
    return output
