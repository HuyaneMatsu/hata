import vampytest

from ....application import Application

from ..fields import put_application


def _iter_options():
    application_id = 202502010001
    name = 'Remilia'
    
    application = Application.precreate(
        application_id,
        name = name,
    )
    
    yield (
        None,
        False,
        {},
    )
    
    yield (
        None,
        True,
        {'application': None},
    )
    
    yield (
        application,
        False,
        {
            'application': {
                'description': '',
                'id': str(application_id),
                'name': name,
                'type': None,
                'verify_key': '',
            }
        },
    )
    
    yield (
        application,
        True,
        {
            'application': {
                'bot_public': False,
                'bot_require_code_grant': False,
                'cover_image': None,
                'description': '',
                'flags': 0,
                'hook': False,
                'id': str(application_id),
                'icon': None,
                'name': name,
                'privacy_policy_url': None,
                'rpc_origins': [],
                'splash': None,
                'tags': [],
                'terms_of_service_url': None,
                'type': None,
                'verify_key': '',
                'embedded_activity_config': None,
                'max_participants': -1,
                'is_monetized': False,
            },
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_application(application, defaults):
    """
    Tests whether ``put_application`` works as intended.
    
    Parameters
    ----------
    application : ``None | Application``
        The application to serialise.
    
    defaults : `bool`
        Whether default values should be included as well.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_application(application, {}, defaults)
