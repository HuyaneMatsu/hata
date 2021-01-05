# -*- coding: utf-8 -*-
from ..extension_loader.snapshot import SNAPSHOT_TAKERS
from .command import CommandProcesser

def take_command_processer_snapshot(client):
    """
    Collects all the commands and categories of a client's command processer.
    
    Parameters
    ----------
    client : ``Client``
        The client, who will be snapshotted.
    
    Returns
    -------
    collected : `None` or `tuple` of `Any`
    """
    command_processer = getattr(client, 'command_processer', None)
    if (command_processer is None) or (not isinstance(command_processer, CommandProcesser)):
        collected = None
    else:
        
        element_category_name_rule = command_processer.category_name_rule
        element_command_error = (command_processer.command_error, command_processer.command_error_checks)
        element_default_event = (command_processer.default_event, command_processer.default_event_checks)
        element_invalid_command = (command_processer.invalid_command, command_processer.invalid_command_checks)
        element_precheck = command_processer.precheck
        element_mention_prefix = command_processer.mention_prefix
        element_prefix = (command_processer._ignorecase, command_processer.prefix, command_processer.prefix_filter)
        element_default_category_name =  command_processer.default_category_name
        
        element_categories = list(command_processer.categories)
        
        element_commands = list()
        for category in element_categories:
            element_commands.extend(category.commands)
        
        collected = element_category_name_rule, element_command_error, element_default_event, element_invalid_command, \
            element_precheck, element_mention_prefix, element_prefix, element_default_category_name, \
            element_categories, element_commands
    
    return collected

def calculate_command_processer_snapshot_difference(client, snapshot_old, snapshot_new):
    """
    Calculates the difference between two command processer snapshots.
    
    Parameters
    ----------
    client : ``Client``
        The respective client.
    snapshot_old : None or `tuple` of `Any`
        An old snapshot taken.
    snapshot_new : None or `tuple` of `Any`
        A new snapshot.
    
    Returns
    -------
    snapshot_difference : `None` or `tuple` of `Any`
    """
    if (snapshot_old is None) or (snapshot_new is None):
        return None
    
    *elements_old, element_categories_old, element_commands_old = snapshot_old
    *elements_new, element_categories_new, element_commands_new = snapshot_new
    
    categories_old = set(element_categories_old)
    categories_new = set(element_categories_new)
    category_interception = categories_old&categories_new
    categories_old -= category_interception
    categories_new -= category_interception
    
    if not categories_old:
        categories_old = None
    
    if not categories_new:
        categories_new = None
    
    if (categories_old is None) and (categories_new is None):
        element_category_difference = None
    else:
        element_category_difference = (categories_old, categories_new)
    
    commands_old = set(element_commands_old)
    command_new = set(element_commands_new)
    command_interception = commands_old&command_new
    commands_old -= command_interception
    command_new -= command_interception
    
    if not commands_old:
        commands_old = None
    
    if not command_new:
        command_new = None
    
    if (categories_old is None) and (command_new is None):
        element_command_difference = None
    else:
        element_command_difference = (commands_old, command_new)
    
    snapshot_difference = (*(None if e1==e2 else e1 for e1, e2 in zip(elements_old, elements_new)),
        element_category_difference, element_command_difference)
    
    return snapshot_difference

def revert_command_processer_snapshot(client, snapshot_difference):
    """
    Reverts a snapshot taken from a command processer.
    
    Parameters
    ----------
    client : ``Client``
        The respective client instance.
    snapshot_difference : `tuple` of `Any`
        The taken snapshot.
    """
    command_processer = getattr(client, 'command_processer', None)
    if (command_processer is None) or (not isinstance(command_processer, CommandProcesser)):
        return
    
    element_category_name_rule_difference, element_command_error_difference, element_default_event_difference, \
        element_invalid_command_difference, element_precheck_difference, element_mention_prefix_difference, \
        element_prefix_difference, element_default_category_name_difference, element_category_difference, \
        element_command_difference = snapshot_difference
    
    if (element_category_name_rule_difference is not None):
        command_processer.category_name_rule = element_category_name_rule_difference
    
    if (element_command_error_difference is not None):
        command_processer.command_error, command_processer.command_error_checks = element_command_error_difference
    
    if (element_default_event_difference is not None):
        command_processer.default_event, command_processer.default_event_checks = element_default_event_difference
    
    if (element_invalid_command_difference is not None):
        command_processer.invalid_command, command_processer.invalid_command_checks = element_invalid_command_difference
    
    if (element_precheck_difference is not None):
        command_processer.precheck = element_precheck_difference
    
    if (element_mention_prefix_difference is not None):
        command_processer.mention_prefix = element_mention_prefix_difference
    
    if (element_prefix_difference is not None):
        command_processer._ignorecase, command_processer.prefix, command_processer.prefix_filter = \
            element_prefix_difference
    
    if (element_default_category_name_difference is not None):
        command_processer.default_category_name = element_default_category_name_difference
    
    if (element_command_difference is not None):
        commands_old, command_new = element_command_difference
        if (command_new is not None):
            for command in command_new:
                try:
                    command_processer._remove_command(command)
                except ValueError:
                    # Ignore conflicts.
                    pass
        
        if (commands_old is not None):
            for command in commands_old:
                try:
                    command_processer._add_command(command)
                except ValueError:
                    # Ignore conflicts.
                    pass
    
    if (element_category_difference is not None):
        categories_old, categories_new = element_category_difference
        if (categories_new is not None):
            for category in categories_new:
                try:
                    command_processer.delete_category(category)
                except ValueError:
                    # Ignore conflicts.
                    pass
        
        if (categories_old is not None):
            for category in categories_old:
                try:
                    command_processer.create_category(category.display_name, check=category.checks,
                        description=category.description)
                except ValueError:
                    # Ignore conflicts.
                    pass


SNAPSHOT_TAKERS['client.command_processer'] = (
    take_command_processer_snapshot,
    calculate_command_processer_snapshot_difference,
    revert_command_processer_snapshot,
        )
