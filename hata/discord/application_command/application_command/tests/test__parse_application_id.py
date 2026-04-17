import vampytest

from ..fields import parse_application_id


def _iter_options():
    application_id = 202302260000

    yield {}, 0
    yield {'application_id': None}, 0
    yield {'application_id': str(application_id)}, application_id


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_application_id(input_data):
    """
    Tests whether ``parse_application_id`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `int`
    """
    return parse_application_id(input_data)
