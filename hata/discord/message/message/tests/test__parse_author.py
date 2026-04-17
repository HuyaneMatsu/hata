import vampytest

from ....user import ClientUserBase, GuildProfile, UserBase, ZEROUSER
from ....webhook import Webhook, WebhookRepr, WebhookType

from ..fields import parse_author


def test__parse_author__none():
    """
    Tests whether ``parse_author`` works as intended.
    
    Case: No data.
    """
    data = {}
    
    user = parse_author(data)

    vampytest.assert_instance(user, UserBase)
    vampytest.assert_is(user, ZEROUSER)


def test__parse_author__webhook():
    """
    Tests whether ``parse_author`` works as intended.

    Case: webhook without user data.
    """
    webhook_id = 202304280025
    
    data = {
        'webhook_id': str(webhook_id),
    }
    
    user = parse_author(data)
    
    vampytest.assert_instance(user, UserBase)
    
    vampytest.assert_instance(user, Webhook)
    vampytest.assert_eq(user.id, webhook_id)
    vampytest.assert_is(user.type, WebhookType.bot)


def test__parse_author__webhook__crosspost():
    """
    Tests whether ``parse_author`` works as intended.

    Case: webhook without user data, crosspost.
    """
    webhook_id = 202304280026
    
    data = {
        'webhook_id': str(webhook_id),
        'message_reference': object(),
    }
    
    user = parse_author(data)
    
    vampytest.assert_instance(user, UserBase)
    
    vampytest.assert_instance(user, Webhook)
    vampytest.assert_eq(user.id, webhook_id)
    vampytest.assert_is(user.type, WebhookType.server)


def test__parse_author__webhook_repr():
    """
    Tests whether ``parse_author`` works as intended.

    Case: webhook with user data.
    """
    webhook_id = 202304280027
    name = 'Keine'
    channel_id = 202304280039
    
    data = {
        'webhook_id': str(webhook_id),
        'author': {
            'id': str(webhook_id),
            'name': name,
        },
    }
    
    user = parse_author(data, channel_id = channel_id)
    
    vampytest.assert_instance(user, UserBase)
    
    vampytest.assert_instance(user, WebhookRepr)
    vampytest.assert_eq(user.id, webhook_id)
    vampytest.assert_is(user.type, WebhookType.bot)
    vampytest.assert_eq(user.name, name)
    vampytest.assert_eq(user.channel_id, channel_id)


def test__parse_author__webhook_repr__crosspost():
    """
    Tests whether ``parse_author`` works as intended.

    Case: webhook with user data, crosspost.
    """
    webhook_id = 202304280028
    name = 'Keine'
    channel_id = 202304280040
    
    data = {
        'webhook_id': str(webhook_id),
        'author': {
            'id': str(webhook_id),
            'name': name,
        },
        'message_reference': object(),
    }
    
    user = parse_author(data, channel_id = channel_id)
    
    vampytest.assert_instance(user, UserBase)
    
    vampytest.assert_instance(user, WebhookRepr)
    vampytest.assert_eq(user.id, webhook_id)
    vampytest.assert_is(user.type, WebhookType.server)
    vampytest.assert_eq(user.name, name)
    vampytest.assert_eq(user.channel_id, channel_id)


def test__parse_author__user__application():
    """
    Tests whether ``parse_author`` works as intended.

    Case: bot user, application command reply.
    """
    user_id = 202304280029
    application_id = 202304280030
    name = 'Keine'
    
    data = {
        'webhook_id': str(application_id),
        'application_id': str(application_id),
        'author': {
            'id': str(user_id),
            'name': name,
        },
    }
    
    user = parse_author(data)
    
    vampytest.assert_instance(user, UserBase)
    
    vampytest.assert_instance(user, ClientUserBase)
    vampytest.assert_eq(user.id, user_id)
    vampytest.assert_eq(user.name, name)


def test__parse_author__application():
    """
    Tests whether ``parse_author`` works as intended.

    Case: bot user without data, application command reply.
    """
    application_id = 202304280032
    
    data = {
        'webhook_id': str(application_id),
        'application_id': str(application_id),
    }
    
    user = parse_author(data)
    
    vampytest.assert_instance(user, UserBase)
    
    vampytest.assert_is(user, ZEROUSER)


def test__parse_author__user():
    """
    Tests whether ``parse_author`` works as intended.

    Case: user.
    """
    user_id = 202304280033
    name = 'Keine'
    
    data = {
        'author': {
            'id': str(user_id),
            'name': name,
        },
    }
    
    user = parse_author(data)
    
    vampytest.assert_instance(user, UserBase)
    
    vampytest.assert_instance(user, ClientUserBase)
    vampytest.assert_eq(user.id, user_id)
    vampytest.assert_eq(user.name, name)


def test__parse_author__webhook__application():
    """
    Tests whether ``parse_author`` works as intended.

    Case: webhook from an application without data.
    """
    webhook_id = 202304280034
    application_id = 202304280035
    
    data = {
        'webhook_id': str(webhook_id),
        'application_id': str(application_id)
    }
    
    user = parse_author(data)
    
    vampytest.assert_instance(user, UserBase)
    
    vampytest.assert_instance(user, Webhook)
    vampytest.assert_eq(user.id, webhook_id)
    vampytest.assert_is(user.type, WebhookType.bot)


def test__parse_author__webhook_repr__application():
    """
    Tests whether ``parse_author`` works as intended.

    Case: webhook from an application without data.
    """
    webhook_id = 202304280036
    application_id = 202304280037
    name = 'Keine'
    channel_id = 202304280038
    
    data = {
        'webhook_id': str(webhook_id),
        'application_id': str(application_id),
        'author': {
            'id': str(webhook_id),
            'name': name,
        },
    }
    
    user = parse_author(data, channel_id = channel_id)
    
    vampytest.assert_instance(user, UserBase)
    
    vampytest.assert_instance(user, WebhookRepr)
    vampytest.assert_eq(user.id, webhook_id)
    vampytest.assert_eq(user.name, name)
    vampytest.assert_is(user.type, WebhookType.bot)
    vampytest.assert_eq(user.channel_id, channel_id)


def test__parse_user__user__guild_profile():
    """
    Tests whether ``parse_user`` works as intended.
    
    Case: user with guild profile.
    """
    user_id = 202304280041
    guild_id = 202304280042
    name = 'Keine'
    nick = 'Oni'
    
    guild_profile = GuildProfile(nick = nick)
    
    data = {
        'author': {
            'name': name,
            'id': str(user_id),
        },
        'member': guild_profile.to_data(
            defaults = True,
            include_internals = True,
        ),
    }
    
    user = parse_author(data, guild_id = guild_id)
    
    vampytest.assert_instance(user, UserBase)
    
    vampytest.assert_instance(user, ClientUserBase)
    vampytest.assert_eq(user.id, user_id)
    vampytest.assert_eq(user.name, name)
    vampytest.assert_eq(user.guild_profiles, {guild_id: guild_profile})
