import vampytest

from scarletio import Future
from scarletio.http_client import HTTPClient

from ...activity import Activity
from ...application import Application
from ...bases import Icon, IconType
from ...color import Color
from ...core import KOKORO
from ...events import IntentFlag
from ...events.event_handler_manager import EventHandlerManager
from ...gateway.client_base import DiscordGatewayClientBase
from ...guild import GuildBadge
from ...http import DiscordApiClient
from ...localization import Locale
from ...user import AvatarDecoration, NamePlate, PremiumType, Status, UserFlag

from ..client import Client
from ..ready_state import ReadyState


def _assert_fields_set(client):
    """
    Asserts whether all fields of the client are set.
    
    Parameters
    ----------
    client : ``Client``
        The client
    """
    vampytest.assert_instance(client, Client)
    vampytest.assert_instance(client._activity, Activity)
    vampytest.assert_instance(client._additional_owner_ids, set, nullable = True)
    vampytest.assert_instance(client._gateway_requesting, bool)
    vampytest.assert_instance(client._gateway_time, float)
    vampytest.assert_instance(client._gateway_url, str)
    vampytest.assert_instance(client._gateway_waiter, Future, nullable = True)
    vampytest.assert_instance(client._should_request_users, bool)
    vampytest.assert_instance(client._status, Status)
    vampytest.assert_instance(client._user_chunker_nonce, int)
    vampytest.assert_instance(client.activities, list, nullable = True)
    vampytest.assert_instance(client.api, DiscordApiClient)
    vampytest.assert_instance(client.application, Application)
    vampytest.assert_instance(client.avatar, Icon)
    vampytest.assert_instance(client.avatar_decoration, AvatarDecoration, nullable = True)
    vampytest.assert_instance(client.name_plate, NamePlate, nullable = True)
    vampytest.assert_instance(client.banner_color, int, nullable = True)
    vampytest.assert_instance(client.banner, Icon)
    vampytest.assert_instance(client.bot, bool)
    vampytest.assert_instance(client.discriminator, int)
    vampytest.assert_instance(client.display_name, str, nullable = True)
    vampytest.assert_instance(client.email, str, nullable = True)
    vampytest.assert_instance(client.email_verified, bool)
    vampytest.assert_instance(client.events, EventHandlerManager)
    vampytest.assert_instance(client.flags, UserFlag)
    vampytest.assert_instance(client.gateway, DiscordGatewayClientBase)
    vampytest.assert_instance(client.group_channels, dict)
    vampytest.assert_instance(client.guild_profiles, dict)
    vampytest.assert_instance(client.guilds, set)
    vampytest.assert_instance(client.http, HTTPClient)
    vampytest.assert_instance(client.id, int)
    vampytest.assert_instance(client.intents, IntentFlag)
    vampytest.assert_instance(client.locale, Locale)
    vampytest.assert_instance(client.mfa_enabled, bool)
    vampytest.assert_instance(client.name, str)
    vampytest.assert_instance(client.premium_type, PremiumType)
    vampytest.assert_instance(client.primary_guild_badge, GuildBadge, nullable = True)
    vampytest.assert_instance(client.private_channels, dict)
    vampytest.assert_instance(client.ready_state, ReadyState, nullable = True)
    vampytest.assert_instance(client.relationships, dict)
    vampytest.assert_instance(client.running, bool)
    vampytest.assert_instance(client.secret, str)
    vampytest.assert_instance(client.shard_count, int)
    vampytest.assert_instance(client.status, Status)
    vampytest.assert_instance(client.statuses, dict, nullable = True)
    vampytest.assert_instance(client.thread_profiles, dict, nullable = True)
    vampytest.assert_instance(client.token, str)
    vampytest.assert_instance(client.voice_clients, dict)


def test__Client__new__no_fields():
    """
    Tests whether ``Client.__new__`` works as intended.
    
    Case: No fields given.
    """
    client = Client(
        token = 'token_20230208_0000',
    )
    
    try:
        _assert_fields_set(client)
    
    # Cleanup
    finally:
        client._delete()
        client = None


def test__Client__new__all_fields():
    """
    Tests whether ``Client.__new__`` works as intended.
    
    Case: All fields given.
    """
    avatar = Icon(IconType.static, 32)
    avatar_decoration = AvatarDecoration(asset = Icon(IconType.static, 2), sku_id = 202310160015)
    banner = Icon(IconType.animated, 12)
    banner_color = Color(1236)
    bot = True
    discriminator = 2222
    display_name = 'Far'
    email = 'rin@orindance.party'
    email_verified = True
    flags = UserFlag(1)
    locale = Locale.greek
    mfa_enabled = True
    name = 'voice in the dark'
    name_plate = NamePlate(
        asset_path = 'koishi/koishi/hat/',
        sku_id = 202506030090,
    )
    premium_type = PremiumType.nitro_basic
    primary_guild_badge = GuildBadge(guild_id = 202405180059, tag = 'meow')

    
    http = HTTPClient(KOKORO)
    api = DiscordApiClient(True, 'koishi', http = http)
    
    client = Client(
        token = 'token_20230208_0001',
        avatar = avatar,
        avatar_decoration = avatar_decoration,
        banner = banner,
        banner_color = banner_color,
        discriminator = discriminator,
        bot = bot,
        display_name = display_name,
        email = email,
        email_verified = email_verified,
        flags = flags,
        locale = locale,
        mfa_enabled = mfa_enabled,
        name = name,
        name_plate = name_plate,
        premium_type = premium_type,
        primary_guild_badge = primary_guild_badge,
        
        api = api,
        http = http,
    )
    
    try:
        _assert_fields_set(client)
            
        vampytest.assert_eq(client.avatar, avatar)
        vampytest.assert_eq(client.avatar_decoration, avatar_decoration)
        vampytest.assert_eq(client.banner, banner)
        vampytest.assert_eq(client.banner_color, banner_color)
        vampytest.assert_eq(client.bot, bot)
        vampytest.assert_eq(client.discriminator, discriminator)
        vampytest.assert_eq(client.display_name, display_name)
        vampytest.assert_eq(client.email, email)
        vampytest.assert_eq(client.email_verified, email_verified)
        vampytest.assert_eq(client.flags, flags)
        vampytest.assert_is(client.locale, locale)
        vampytest.assert_eq(client.mfa_enabled, mfa_enabled)
        vampytest.assert_eq(client.name, name)
        vampytest.assert_eq(client.name_plate, name_plate)
        vampytest.assert_is(client.premium_type, premium_type)
        vampytest.assert_eq(client.primary_guild_badge, primary_guild_badge)
    
        
        vampytest.assert_is(client.api, api)
        vampytest.assert_is(client.http, http)
    
    # Cleanup
    finally:
        client._delete()
        client = None
