import vampytest

from .. import InteractionEvent


def test__InteractionEvent__repr():
    """
    Tests whether ``InteractionEvent``'s ``__repr__` method works as expected.
    """
    data = {
        'application_id': '775799577604522054',
        'channel_id': '772908445358620702',
        'data': {
            'id': '866818195033292850',
            'name': 'context-menu-user-2',
            'resolved': {
                'members': {
                    '809850198683418695': {
                        'avatar': None,
                        'is_pending': False,
                        'joined_at': '2021-02-12T18:25:07.972000+00:00',
                        'nick': None,
                        'pending': False,
                        'permissions': '246997699136',
                        'premium_since': None,
                        'roles': [],
                    }
                },
                'users': {
                    '809850198683418695': {
                        'avatar': 'afc428077119df8aabbbd84b0dc90c74',
                        'bot': True,
                        'discriminator': '7302',
                        'id': '809850198683418695',
                        'public_flags': 0,
                        'username': 'VoltyDemo',
                    }
                }
            },
            'target_id': '809850198683418695',
            'type': 2,
        },
        'guild_id': '772904309264089089',
        'guild_locale': 'en-US',
        'app_permissions': '442368',
        'id': '867794291820986368',
        'locale': 'en-US',
        'member': {
            'avatar': None,
            'deaf': False,
            'is_pending': False,
            'joined_at': '2020-11-02T20:46:57.364000+00:00',
            'mute': False,
            'nick': None,
            'pending': False,
            'permissions': '274877906943',
            'premium_since': None,
            'roles': [
                '785609923542777878',
            ],
            'user': {
                'avatar': 'a_f03401914fb4f3caa9037578ab980920',
                'discriminator': '6538',
                'id': '167348773423415296',
                'public_flags': 1,
                'username': 'ian',
            }
        },
        'token': 'UNIQUE_TOKEN',
        'type': 2,
        'version': 1,
    }
    
    event = InteractionEvent(data)
    
    vampytest.assert_instance(repr(event), str)
