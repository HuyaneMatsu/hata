# -*- coding: utf-8 -*-

# Upgraded commands extension for hata.
# Work in progress.

from functools import partial as partial_func

from .checks import *
from .utils import *

__all__ = (
    'custom_check',
    'has_any_role',
    'has_client_guild_permission',
    'has_client_permission',
    'has_guild_permission',
    'has_permission',
    'has_role',
    'is_announcement_channel',
    'is_any_category',
    'is_any_channel',
    'is_any_guild',
    'is_booster',
    'is_bot_account',
    'is_category',
    'is_channel',
    'is_client',
    'is_guild',
    'is_guild_owner',
    'is_in_guild',
    'is_in_private',
    'is_in_voice',
    'is_nsfw_channel',
    'is_owner',
    'is_owner_or_has_any_role',
    'is_owner_or_has_guild_permission',
    'is_owner_or_has_permission',
    'is_owner_or_has_role',
    'is_owner_or_is_guild_owner',
    'is_user_account',
    'is_user_account_or_is_client',
    *checks.__all__,
    *utils.__all__,
)


from .checks import CheckHasRole, CheckIsOwnerOrHasRole, CheckHasAnyRole, CheckIsOwnerOrHasAnyRole, CheckIsInGuild, \
    CheckIsInPrivate, CheckIsOwner, CheckIsGuildOwner, CheckIsOwnerOrIsGuildOwner, CheckHasPermission, \
    CheckIsOwnerOrHasPermission, CheckHasGuildPermission, CheckIsOwnerHasGuildPermission, CheckHasClientPermission, \
    CheckHasClientGuildPermission, CheckIsGuild, CheckIsAnyGuild, CheckCustom, CheckIsChannel, CheckIsAnyChannel, \
    CheckIsNsfwChannel, CheckIsAnnouncementChannel, CheckIsInVoice, CheckIsBooster, CheckIsClient, CheckUserAccount, \
    CheckBotAccount, CheckIsUserAccountOrIsClient, CheckIsCategory, CheckIsAnyCategory


has_role = partial_func(CommandCheckWrapper, CheckHasRole)
is_owner_or_has_role = partial_func(CommandCheckWrapper, CheckIsOwnerOrHasRole)
has_any_role = partial_func(CommandCheckWrapper, CheckHasAnyRole)
is_owner_or_has_any_role = partial_func(CommandCheckWrapper, CheckIsOwnerOrHasAnyRole)
is_in_guild = partial_func(CommandCheckWrapper, CheckIsInGuild)
is_in_private = partial_func(CommandCheckWrapper, CheckIsInPrivate)
is_owner = partial_func(CommandCheckWrapper, CheckIsOwner)
is_guild_owner = partial_func(CommandCheckWrapper, CheckIsGuildOwner)
is_owner_or_is_guild_owner = partial_func(CommandCheckWrapper, CheckIsOwnerOrIsGuildOwner)
has_permission = partial_func(CommandCheckWrapper, CheckHasPermission)
is_owner_or_has_permission = partial_func(CommandCheckWrapper, CheckIsOwnerOrHasPermission)
has_guild_permission = partial_func(CommandCheckWrapper, CheckHasGuildPermission)
is_owner_or_has_guild_permission = partial_func(CommandCheckWrapper, CheckIsOwnerHasGuildPermission)
has_client_permission = partial_func(CommandCheckWrapper, CheckHasClientPermission)
has_client_guild_permission = partial_func(CommandCheckWrapper, CheckHasClientGuildPermission)
is_guild = partial_func(CommandCheckWrapper, CheckIsGuild)
is_any_guild = partial_func(CommandCheckWrapper, CheckIsAnyGuild)
custom_check = partial_func(CommandCheckWrapper, CheckCustom)
is_channel = partial_func(CommandCheckWrapper, CheckIsChannel)
is_any_channel = partial_func(CommandCheckWrapper, CheckIsAnyChannel)
is_nsfw_channel = partial_func(CommandCheckWrapper, CheckIsNsfwChannel)
is_announcement_channel = partial_func(CommandCheckWrapper, CheckIsAnnouncementChannel)
is_in_voice = partial_func(CommandCheckWrapper, CheckIsInVoice)
is_booster = partial_func(CommandCheckWrapper, CheckIsBooster)
is_client = partial_func(CommandCheckWrapper, CheckIsClient)
is_user_account = partial_func(CommandCheckWrapper, CheckUserAccount)
is_bot_account = partial_func(CommandCheckWrapper, CheckBotAccount)
is_user_account_or_is_client = partial_func(CommandCheckWrapper, CheckIsUserAccountOrIsClient)
is_category = partial_func(CommandCheckWrapper, CheckIsCategory)
is_any_category = partial_func(CommandCheckWrapper, CheckIsAnyCategory)
