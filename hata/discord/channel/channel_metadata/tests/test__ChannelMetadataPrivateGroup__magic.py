import vampytest

from ....bases import Icon, IconType
from ....user import User

from ..private_group import ChannelMetadataPrivateGroup


def test__ChannelMetadataPrivateGroup__repr():
    """
    Tests whether ``.ChannelMetadataPrivateGroup.__repr__`` works as intended.
    """
    application_id = 202301210004
    users = [User.precreate(202209160017)]
    owner_id = 202209160020
    icon = Icon(IconType.static, 1)
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataPrivateGroup(
        application_id = application_id,
        users = users,
        owner_id = owner_id,
        name = name,
        icon = icon,
    )
    
    vampytest.assert_instance(repr(channel_metadata), str)


def test__ChannelMetadataPrivateGroup__hash():
    """
    Tests whether ``.ChannelMetadataPrivateGroup.__hash__`` works as intended.
    """
    application_id = 202301210005
    users = [User.precreate(202209180118)]
    owner_id = 20220918119
    icon = Icon(IconType.static, 1)
    name = 'Armelyrics'
    
    channel_metadata = ChannelMetadataPrivateGroup(
        application_id = application_id,
        users = users,
        owner_id = owner_id,
        name = name,
        icon = icon,
    )
    
    vampytest.assert_instance(hash(channel_metadata), int)


def _iter_options__eq():
    application_id = 202301210006
    user_0 = User.precreate(202209160018)
    user_1 = User.precreate(202209160019)
    owner_id = 202209160021
    icon = Icon(IconType.static, 1)
    name = 'Armelyrics'
    
    keyword_parameters = {
        'application_id': application_id,
        'users': [user_0],
        'owner_id': owner_id,
        'name': name,
        'icon': icon,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'users': [user_1],
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'owner_id': 202209160022,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'icon': Icon(IconType.static, 2),
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'name': 'Okuu',
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'application_id': 202301210007,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ChannelMetadataPrivateGroup__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ChannelMetadataPrivateGroup.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    channel_metadata_0 = ChannelMetadataPrivateGroup(**keyword_parameters_0)
    channel_metadata_1 = ChannelMetadataPrivateGroup(**keyword_parameters_1)
    
    output = channel_metadata_0 == channel_metadata_1
    vampytest.assert_instance(output, bool)
    return output
