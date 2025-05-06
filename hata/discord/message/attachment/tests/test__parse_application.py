import vampytest

from ....application import Application

from ..fields import parse_application


def _iter_options():
    application_id = 202502010000
    application = Application.precreate(application_id)
    
    yield {}, None
    yield {'application': None}, None
    yield {'application': {'id': str(application_id)}}, application


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_application(input_data):
    """
    Tests whether ``parse_application`` works as intended.
    
    Parameters
    ----------
    input_data : `dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | Application`
    """
    output = parse_application(input_data)
    vampytest.assert_instance(output, Application, nullable = True)
    return output
