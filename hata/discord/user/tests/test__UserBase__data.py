import vampytest

from .. import UserBase


def test__UserBase__to_data():
    """
    Tests whether ``UserBase``'s `.to_data` method works as expected.
    """
    user_base = UserBase._create_empty(1)
    user_base._update_attributes({
        'avatar': "7771adba8a47a6409086746c9c29c108",
        'discriminator': '2016',
        'id': '1',
        'public_flags': 0,
        'username': 'owo',
        'accent_color': 123,
        'banner': None,
    })
    
    vampytest.assert_eq(
        user_base.to_data(),
        {
            'avatar': "7771adba8a47a6409086746c9c29c108",
            'discriminator': '2016',
            'id': '1',
            'flags': 0,
            'name': 'owo',
            'accent_color': 123,
            'banner': None,
        }
    )
