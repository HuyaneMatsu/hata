import vampytest

from ...message_application import MessageApplication

from ..fields import parse_application


def _iter_options():
    application_id = 202304290003
    application = MessageApplication.precreate(application_id, name = 'orin')
    
    yield {}, None
    yield {'application': None}, None
    yield {'application': application.to_data()}, application


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
    output : `None | MessageApplication`
    """
    output = parse_application(input_data)
    vampytest.assert_instance(output, MessageApplication, nullable = True)
    return output
