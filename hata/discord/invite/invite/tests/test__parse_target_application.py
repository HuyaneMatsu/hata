import vampytest

from ....application import Application

from ..fields import parse_target_application


def _iter_options():
    application_id = 202308030000
    application = Application.precreate(application_id)
    
    yield {}, None
    yield {'target_application': None}, None
    yield {'target_application': {'id': str(application_id)}}, application


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_target_application(input_data):
    """
    Tests whether ``parse_target_application`` works as intended.
    
    Parameters
    ----------
    input_data : `str`
        Data to parse from.
    
    Returns
    -------
    output : `None`, ``Application``
    """
    return parse_target_application(input_data)
