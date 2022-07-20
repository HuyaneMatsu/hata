__all__ = ()

from ..helpers import render_main_call_into

from .render_constants import (
    BOX_BOTTOM, BOX_LEFT, BOX_LEFT_BOT, BOX_LEFT_TOP, BOX_RIGHT, BOX_RIGHT_BOT, BOX_RIGHT_TOP, BOX_TITLE_ERROR,
    BOX_TITLE_SUB_COMMANDS, BOX_TOP
)


def render_usage_line_into(into, name_trace_iterator):
    """
    Renders the command usage line into the given list.
    
    Parameters
    ----------
    into : `list` of `str`
        The list to render the usage into.
    name_trace_iterator : `None`, `GeneratorType`
        Name trace iterator for looking up the command's access trace.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append('Usage: ')
    render_main_call_into(into)
    
    if (name_trace_iterator is not None):
        for name in name_trace_iterator:
            into.append(' ')
            into.append(name)
    
    return into


def render_sub_command_box_into(into, sub_command_names, line_length):
    """
    Renders the sub-command box into the given list.
    
    Parameters
    ----------
    into : `list` of `str`
        The list to render the usage into.
    sub_command_names : `str`
        The sub command names to render.
    line_length : `str`
        The expected length of every line.
    
    Returns
    -------
    into : `list` of `str`
    """
    into = render_box_start_into(into, line_length, BOX_TITLE_SUB_COMMANDS)
    
    # Render line n
    for sub_command_name in sub_command_names:
        into.append(BOX_LEFT)
        into.append(sub_command_name)
        into = render_box_line_adjustment_into(into, len(sub_command_name), line_length)
        into.append(BOX_RIGHT)
        into.append('\n')
    
    # Render line -1
    into = render_box_end_into(into, line_length)

    return into


def render_box_start_into(into, line_length, title):
    """
    Renders box start into the given list.
    
    Parameters
    ----------
    into : `list` of `str`
        The list of strings to render to.
    line_length : `int`
        The expected length of the line.
    title : `str`
        Title of the box.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append(BOX_LEFT_TOP)
    into.append(title)
    
    line_adjust = line_length - len(title)
    if line_adjust > 0:
        into.append(BOX_TOP * line_adjust)
    
    into.append(BOX_RIGHT_TOP)
    into.append('\n')
    
    return into


def render_box_line_adjustment_into(into, local_line_length, global_line_length):
    """
    Renders box line adjustment into the given list.
    
    Parameters
    ----------
    into : `list` of `str`
        The list of strings to render to.
    local_line_length : `int`
        The expected length of the line locally.
    global_line_length : `int`
        The global line length,
    
    Returns
    -------
    into : `list` of `str`
    """
    line_adjust = global_line_length - local_line_length
    if line_adjust > 0:
        into.append(' ' * line_adjust)
    
    return into


def render_box_end_into(into, line_length):
    """
    Renders box end into the given list.
    
    Parameters
    ----------
    into : `list` of `str`
        The list of strings to render to.
    line_length : `int`
        The expected length of the line.
    
    Returns
    -------
    into : `list` of `str`
    """
    into.append(BOX_LEFT_BOT)
    into.append(BOX_BOTTOM * line_length)
    into.append(BOX_RIGHT_BOT)
    into.append('\n')
    
    return into


def render_error_box_into_single_line(into, line):
    """
    Renders an error message box into the given list.
    
    Parameters
    ----------
    into : `list` of `str`
        The list of strings to render to.
    line : `str`
        The message to show.
    
    Returns
    -------
    into : `list` of `str`
    """
    return render_error_box_into_multi_line(into, [line])


def render_error_box_into_multi_line(into, lines):
    """
    Renders an error message box of multiple lines into the given list.
    
    Parameters
    ----------
    into : `list` of `str`
        The list of strings to render to.
    message : `list` of `str`
        The message lines to show.
    
    Returns
    -------
    into : `list` of `str`
    """
    line_length = max(len(line) for line in lines)
    line_length = max(line_length, len(BOX_TITLE_ERROR))
    
    into = render_box_start_into(into, line_length, BOX_TITLE_ERROR)
    
    for line in lines:
        into.append(BOX_LEFT)
        into.append(line)
        into = render_box_line_adjustment_into(into, len(line), line_length)
        into.append(BOX_RIGHT)
        into.append('\n')
    
    into = render_box_end_into(into, line_length)
    return into
