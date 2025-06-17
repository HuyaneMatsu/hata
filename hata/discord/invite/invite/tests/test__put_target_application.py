import vampytest

from ....application import Application

from ..fields import put_target_application


def _iter_options():
    yield None, False, {}
    yield None, True, {'target_application': None}
    
    application_id = 202308030001
    name = 'Remilia'
    
    application = Application.precreate(
        application_id,
        name = name,
    )
    
    expected_output = {
        'target_application': {
            'description': '',
            'id': str(application_id),
            'name': name,
            'type': None,
            'verify_key': '',
        }
    }
    
    yield application, False, expected_output
    
    expected_output = {
        'target_application': {
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
    }
    
    yield application, True, expected_output


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_target_application(application, defaults):
    """
    Tests whether ``put_target_application`` works as intended.
    
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
    return put_target_application(application, {}, defaults)
