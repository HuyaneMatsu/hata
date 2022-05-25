__all__ = ('PermissionMismatchWarning',)

import warnings

from ...discord.application import Team


class PermissionMismatchWarning(RuntimeWarning):
    """
    Warnings used when an application has different permissions than expected.
    """


def _maybe_render_application_command_permission_overwrites_to(
    title_line, application_command_permission_overwrites, into
):
    """
    Renders the given permission overwrites to the given list of strings.
    
    Parameters
    ----------
    application_command_permission_overwrites : `set` of ``ApplicationCommandPermissionOverwrite``
        The permission overwrites to show.
    into : `list` of `str`
        The list to render the representation of the application command permission overwrites to.
    
    Returns
    -------
    into : `list` of `str`
    """
    if application_command_permission_overwrites:
        into.append('\n')
        into.append(title_line)
        
        into = _render_application_command_permission_overwrites_to(application_command_permission_overwrites, into)
        
    return into


def _render_application_command_permission_overwrites_to(application_command_permission_overwrites, into):
    """
    Renders the given permission overwrites to the given list of strings.
    
    Parameters
    ----------
    application_command_permission_overwrites : `set` of ``ApplicationCommandPermissionOverwrite``
        The permission overwrites to show.
    into : `list` of `str`
        The list to render the representation of the application command permission overwrites to.
    
    Returns
    -------
    into : `list` of `str`
    """
    for index, application_command_permission_overwrite in (
        enumerate(sorted(application_command_permission_overwrites), 1)
    ):
        index_name = str(index)
        into.append('\n')
        into.append(index_name)
        into.append(':')
        into.append(' ' * max(0, 3 - len(index_name)))
        into.append('target type = ')
        into.append(application_command_permission_overwrite.target_type.name)
        into.append('\n    target id = ')
        into.append(str(application_command_permission_overwrite.target_id))
        into.append('\n    allow = ')
        into.append('true' if application_command_permission_overwrite.allow else 'false')
    
    return into


def create_permission_mismatch_message(
    application_command,
    guild_id,
    current_application_command_permission_overwrites,
    expected_application_command_permission_overwrites
):
    """
    Creates permission mismatch message.
    
    Parameters
    ----------
    application_command : ``ApplicationCommand``
        The respective application command-
    guild_id : `int`
        The respective guild's identifier where the command is.
    current_application_command_permission_overwrites : `None`, `list` of ``ApplicationCommandPermissionOverwrite``
        The actual permission overwrites of the command.
    expected_application_command_permission_overwrites : `None`, `list` of ``ApplicationCommandPermissionOverwrite``
        The expected permission overwrites of the command.
    
    Returns
    -------
    message : `str`
    """
    message_parts = []
    
    message_parts.append('\nApplication command permission mismatch at:')
    
    message_parts.append('\n    guild id = ')
    message_parts.append(str(guild_id))
    
    message_parts.append('\n    command id = ')
    message_parts.append(str(application_command.id))
    
    message_parts.append('\n    command name = ')
    message_parts.append(str(application_command.name))
    
    
    if current_application_command_permission_overwrites is None:
        current_application_command_permission_overwrites = set()
    else:
        current_application_command_permission_overwrites = {*current_application_command_permission_overwrites}
    
    if expected_application_command_permission_overwrites is None:
        expected_application_command_permission_overwrites = set()
    else:
        expected_application_command_permission_overwrites = {*expected_application_command_permission_overwrites}
    
    
    message_parts = _maybe_render_application_command_permission_overwrites_to(
        'Shared application command permission overwrites:',
        current_application_command_permission_overwrites & expected_application_command_permission_overwrites,
        message_parts,
    )
    
    message_parts = _maybe_render_application_command_permission_overwrites_to(
        'Additional application command permission overwrites:',
        current_application_command_permission_overwrites - expected_application_command_permission_overwrites,
        message_parts,
    )
    
    message_parts = _maybe_render_application_command_permission_overwrites_to(
        'Missing application command permission overwrites:',
        expected_application_command_permission_overwrites - current_application_command_permission_overwrites,
        message_parts,
    )
    
    
    return ''.join(message_parts)


def check_and_warn_can_request_owners_access_of(client):
    """
    Checks whether the client's access can be requested. If it cannot drops a warning.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    
    Returns
    -------
    can_request_owners_access : `bool`
    """
    while True:
        secret = client.secret
        if secret is None:
            failure_reason = '`client.secret` is None`.'
            break
        
        if isinstance(client.application.owner, Team):
            failure_reason = 'Client application owned by team.'
            break
        
        failure_reason = True
        break
    
    if failure_reason is None:
        return True
    
    
    warnings.warn(
        (
            f'\n'
            f'Requesting owner\'s access impossible:\n'
            f'reason = {failure_reason}\n'
            f'client = {client!r}'
        ),
        PermissionMismatchWarning,
    )
    return False
