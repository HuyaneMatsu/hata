__all__ = ('create_ansi_format_code',)


def create_ansi_format_code(text_decoration = None, background_color = None, foreground_color = None):
    """
    Creates an ansi text format code for `ansi` codeblocks.
    
    > If no parameter is given, will generate a format reset code.
    
    Parameters
    ----------
    text_decoration : `None`, ``AnsiTextDecoration`` = `None`, Optional
        Text decoration.
    
    background_color : `None`, ``AnsiBackgroundColor`` = `None`, Optional
        background color.
    
    foreground_color : `None`, ``AnsiForegroundColor`` = `None`, Optional
        Foreground color.
    
    Returns
    -------
    format_code : `str`
    """
    format_code_parts = ['\u001b[']
    
    field_added = False
    
    if (text_decoration is not None):
        field_added = True
        
        format_code_parts.append(str(text_decoration.value))
    
    if (background_color is not None):
        if field_added:
            format_code_parts.append(';')
        else:
            field_added = True
        
        format_code_parts.append(str(background_color.value))
    
    if (foreground_color is not None):
        if field_added:
            format_code_parts.append(';')
        else:
            field_added = True
        
        format_code_parts.append(str(foreground_color.value))
    
    if not field_added:
        format_code_parts.append('0')
    
    format_code_parts.append('m')
    
    return ''.join(format_code_parts)
