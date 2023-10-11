import vampytest

from ...message_application import MessageApplication

from ..fields import put_application_into


def _iter_options():
    application_id = 202304290004
    application = MessageApplication.precreate(application_id, name = 'Orin')
    
    yield (None, False, {})
    yield (None, True, {'application': None})
    yield (application, False, {'application': application.to_data(include_internals = True)})
    yield (application, True, {'application': application.to_data(defaults = True, include_internals = True)})


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_application_into(input_value, defaults):
    """
    Tests whether ``put_application_into`` is working as intended.
    
    Parameters
    ----------
    input_value : ``None | MessageApplication``
        The value to serialise.
    defaults : `bool`
        Whether fields of their default value should be included in the output.
    
    Returns
    -------
    data : `dict<str, object>`
    """
    return put_application_into(input_value, {}, defaults)
