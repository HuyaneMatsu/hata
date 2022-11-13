import vampytest

from ...localization import Locale
from ...localization.utils import destroy_locale_dictionary
from ...permission import Permission

from .. import ApplicationCommand, ApplicationCommandOption, ApplicationCommandOptionType, ApplicationCommandTargetType


def test_ApplicationCommand__from_data__0():
    """
    Tests whether ``ApplicationCommand.from_data`` works as intended when all the fields are given.
    """
    name = 'owo'
    description = 'description'
    allow_in_dm = True
    description_localizations = {
        Locale.thai: 'ayy',
        Locale.czech: 'yay',
    }
    name_localizations = {
        Locale.thai: 'nay',
        Locale.czech: 'lay',
    }
    nsfw = True
    options = [
        ApplicationCommandOption(
            'option',
            'optional',
            ApplicationCommandOptionType.string,

        )
    ]
    required_permissions = Permission().update_by_keys(administrator = True)
    target_type = ApplicationCommandTargetType.chat
    
    application_command_id = 202209030002
    application_id = 202209030003
    guild_id = 202209030004
    version = 2
    
    application_command = ApplicationCommand.from_data({
        'id': str(application_command_id),
        'application_id': str(application_id),
        'guild_id': str(guild_id),
        'dm_permission': allow_in_dm,
        'description': description,
        'description_localizations': destroy_locale_dictionary(description_localizations),
        'name': name,
        'name_localizations': destroy_locale_dictionary(name_localizations),
        'nsfw': nsfw,
        'options': [option.to_data() for option in options],
        'default_member_permissions': format(required_permissions, 'd'),
        'type': target_type.value,
        'version': version,
    })
    
    vampytest.assert_eq(application_command.name, name)
    vampytest.assert_eq(application_command.description, description)
    vampytest.assert_eq(application_command.allow_in_dm, allow_in_dm)
    vampytest.assert_eq(application_command.description_localizations, description_localizations)
    vampytest.assert_eq(application_command.name_localizations, name_localizations)
    vampytest.assert_eq(application_command.nsfw, nsfw)
    vampytest.assert_eq(application_command.options, options)
    vampytest.assert_eq(application_command.required_permissions, required_permissions)
    vampytest.assert_is(application_command.target_type, target_type)
    
    # Also test the extra fields whether they are set.
    vampytest.assert_eq(application_command.id, application_command_id)
    vampytest.assert_eq(application_command.application_id, application_id)
    vampytest.assert_eq(application_command.guild_id, guild_id)
    vampytest.assert_eq(application_command.version, version)


def test__ApplicationCommand__update_attributes():
    """
    Tests whether `ApplicationCommand._update_attributes` works as intended.
    """
    old_name = 'owo'
    new_name = 'uwu'
    old_description = 'description'
    new_description = 'mars'
    old_allow_in_dm = True
    new_allow_in_dm = False
    old_description_localizations = {
        Locale.thai: 'ayy',
        Locale.czech: 'yay',
    }
    new_description_localizations = {
        Locale.dutch: 'aya',
        Locale.greek: 'yya',
    }
    old_name_localizations = {
        Locale.thai: 'nay',
        Locale.czech: 'lay',
    }
    new_name_localizations = {
        Locale.dutch: 'aya',
        Locale.greek: 'yya',
    }
    old_nsfw = True
    new_nsfw = False
    old_options = [
        ApplicationCommandOption(
            'option',
            'optional',
            ApplicationCommandOptionType.string,

        )
    ]
    new_options = [
        ApplicationCommandOption(
            'hello',
            'hell',
            ApplicationCommandOptionType.float,

        )
    ]
    old_required_permissions = Permission().update_by_keys(administrator = True)
    new_required_permissions = Permission().update_by_keys(kick_users=True)
    old_target_type = ApplicationCommandTargetType.chat
    new_target_type = ApplicationCommandTargetType.message
    
    
    application_command_id = 202209030005
    application_id = 202209030006
    guild_id = 202209030007
    version = 2

    application_command = ApplicationCommand.from_data({
        'id': str(application_command_id),
        'application_id': str(application_id),
        'guild_id': str(guild_id),
        'dm_permission': old_allow_in_dm,
        'description': old_description,
        'description_localizations': destroy_locale_dictionary(old_description_localizations),
        'name': old_name,
        'name_localizations': destroy_locale_dictionary(old_name_localizations),
        'nsfw': old_nsfw,
        'options': [option.to_data() for option in old_options],
        'default_member_permissions': format(old_required_permissions, 'd'),
        'type': old_target_type.value,
        'version': version,
    })
    
    application_command._update_attributes({
        'dm_permission': new_allow_in_dm,
        'description': new_description,
        'description_localizations': destroy_locale_dictionary(new_description_localizations),
        'name': new_name,
        'name_localizations': destroy_locale_dictionary(new_name_localizations),
        'nsfw': new_nsfw,
        'options': [option.to_data() for option in new_options],
        'default_member_permissions': format(new_required_permissions, 'd'),
        'type': new_target_type.value,
    })
    
    vampytest.assert_eq(application_command.name, new_name)
    vampytest.assert_eq(application_command.description, new_description)
    vampytest.assert_eq(application_command.allow_in_dm, new_allow_in_dm)
    vampytest.assert_eq(application_command.description_localizations, new_description_localizations)
    vampytest.assert_eq(application_command.name_localizations, new_name_localizations)
    vampytest.assert_eq(application_command.nsfw, new_nsfw)
    vampytest.assert_eq(application_command.options, new_options)
    vampytest.assert_eq(application_command.required_permissions, new_required_permissions)
    vampytest.assert_is(application_command.target_type, new_target_type)


def test__ApplicationCommand__difference_update_attributes():
    """
    Tests whether `ApplicationCommand._difference_update_attributes` works as intended.
    """
    old_name = 'owo'
    new_name = 'uwu'
    old_description = 'description'
    new_description = 'mars'
    old_allow_in_dm = True
    new_allow_in_dm = False
    old_description_localizations = {
        Locale.thai: 'ayy',
        Locale.czech: 'yay',
    }
    new_description_localizations = {
        Locale.dutch: 'aya',
        Locale.greek: 'yya',
    }
    old_name_localizations = {
        Locale.thai: 'nay',
        Locale.czech: 'lay',
    }
    new_name_localizations = {
        Locale.dutch: 'aya',
        Locale.greek: 'yya',
    }
    old_nsfw = True
    new_nsfw = False
    old_options = [
        ApplicationCommandOption(
            'option',
            'optional',
            ApplicationCommandOptionType.string,

        )
    ]
    new_options = [
        ApplicationCommandOption(
            'hello',
            'hell',
            ApplicationCommandOptionType.float,

        )
    ]
    old_required_permissions = Permission().update_by_keys(administrator = True)
    new_required_permissions = Permission().update_by_keys(kick_users=True)
    old_target_type = ApplicationCommandTargetType.chat
    new_target_type = ApplicationCommandTargetType.message
    
    
    application_command_id = 202209030008
    application_id = 202209030009
    guild_id = 202209030010
    version = 2

    application_command = ApplicationCommand.from_data({
        'id': str(application_command_id),
        'application_id': str(application_id),
        'guild_id': str(guild_id),
        'dm_permission': old_allow_in_dm,
        'description': old_description,
        'description_localizations': destroy_locale_dictionary(old_description_localizations),
        'name': old_name,
        'name_localizations': destroy_locale_dictionary(old_name_localizations),
        'nsfw': old_nsfw,
        'options': [option.to_data() for option in old_options],
        'default_member_permissions': format(old_required_permissions, 'd'),
        'type': old_target_type.value,
        'version': version,
    })
    
    old_attributes = application_command._difference_update_attributes({
        'dm_permission': new_allow_in_dm,
        'description': new_description,
        'description_localizations': destroy_locale_dictionary(new_description_localizations),
        'name': new_name,
        'name_localizations': destroy_locale_dictionary(new_name_localizations),
        'nsfw': new_nsfw,
        'options': [option.to_data() for option in new_options],
        'default_member_permissions': format(new_required_permissions, 'd'),
        'type': new_target_type.value,
    })
    
    vampytest.assert_eq(application_command.name, new_name)
    vampytest.assert_eq(application_command.description, new_description)
    vampytest.assert_eq(application_command.allow_in_dm, new_allow_in_dm)
    vampytest.assert_eq(application_command.description_localizations, new_description_localizations)
    vampytest.assert_eq(application_command.name_localizations, new_name_localizations)
    vampytest.assert_eq(application_command.nsfw, new_nsfw)
    vampytest.assert_eq(application_command.options, new_options)
    vampytest.assert_eq(application_command.required_permissions, new_required_permissions)
    vampytest.assert_eq(application_command.target_type, new_target_type)
    
    vampytest.assert_in('name', old_attributes)
    vampytest.assert_in('description', old_attributes)
    vampytest.assert_in('allow_in_dm', old_attributes)
    vampytest.assert_in('description_localizations', old_attributes)
    vampytest.assert_in('name_localizations', old_attributes)
    vampytest.assert_in('nsfw', old_attributes)
    vampytest.assert_in('options', old_attributes)
    vampytest.assert_in('required_permissions', old_attributes)
    vampytest.assert_in('target_type', old_attributes)

    vampytest.assert_eq(old_attributes['name'], old_name)
    vampytest.assert_eq(old_attributes['description'], old_description)
    vampytest.assert_eq(old_attributes['allow_in_dm'], old_allow_in_dm)
    vampytest.assert_eq(old_attributes['description_localizations'], old_description_localizations)
    vampytest.assert_eq(old_attributes['name_localizations'], old_name_localizations)
    vampytest.assert_eq(old_attributes['nsfw'], old_nsfw)
    vampytest.assert_eq(old_attributes['options'], old_options)
    vampytest.assert_eq(old_attributes['required_permissions'], old_required_permissions)
    vampytest.assert_is(old_attributes['target_type'], old_target_type)


def test_ApplicationCommand__to_data__0():
    """
    Tests whether ``ApplicationCommand.to_data`` works as intended when all the fields are given.
    """
    name = 'owo'
    description = 'description'
    allow_in_dm = True
    description_localizations = {
        Locale.thai: 'ayy',
        Locale.czech: 'yay',
    }
    name_localizations = {
        Locale.thai: 'nay',
        Locale.czech: 'lay',
    }
    nsfw = True
    options = [
        ApplicationCommandOption(
            'option',
            'optional',
            ApplicationCommandOptionType.string,

        )
    ]
    required_permissions = Permission().update_by_keys(administrator = True)
    target_type = ApplicationCommandTargetType.chat
    
    application_command_id = 202209030011
    application_id = 202209030012
    guild_id = 202209030013
    version = 2
    
    data = {
        'dm_permission': allow_in_dm,
        'description': description,
        'description_localizations': destroy_locale_dictionary(description_localizations),
        'name': name,
        'name_localizations': destroy_locale_dictionary(name_localizations),
        'nsfw': nsfw,
        'options': [option.to_data() for option in options],
        'default_member_permissions': format(required_permissions, 'd'),
        'type': target_type.value,
    }
    
    extra_fields = {
        'id': str(application_command_id),
        'application_id': str(application_id),
        'guild_id': str(guild_id),
        'version': version,
    }
    
    application_command = ApplicationCommand.from_data({**data, **extra_fields})
    new_data = application_command.to_data()
    
    # `default_permission` is deprecated, pop it
    new_data.pop('default_permission')
    
    vampytest.assert_eq(data, new_data)
