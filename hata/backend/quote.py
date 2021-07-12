__all__ = ()

from string import ascii_letters, ascii_lowercase, digits

BIN_ASCII_LOWERCASE = ascii_lowercase.encode('ascii')
BIN_PERCENTAGE_ALLOWED = {f'%{index:02X}'.encode('ascii') for index in range(256)}
GEN_DELIMS = ':/?#[]@'
SUB_DELIMS_WO_QS = '!$\'()*,;'
QUERY_STRING_NOT_SAFE = '+&='
SUB_DELIMS = f'{SUB_DELIMS_WO_QS}{QUERY_STRING_NOT_SAFE}'
RESERVED = f'{GEN_DELIMS}{SUB_DELIMS}'
UNRESERVED = f'{ascii_letters}{digits}-._~'
ALLOWED = f'{UNRESERVED}{SUB_DELIMS_WO_QS}'


def quote(value, safe='', protected='', query_string=False):
    """
    Http quotes the given `value`.
    
    Parameters
    ----------
    value : `str`
        The value to quote.
    safe : `str`, Optional
        Additional percentage encoding safe characters. Defaults to empty string.
    protected : `str`, Optional
        Additional character to have percentage encoding preference. Defaults to empty string.
    query_string : `bool`, Optional
        Whether the generated value is a query string key or value. Defaults to `False`
    
    Returns
    -------
    quoted : `str`
        The quoted value.
    
    Raises
    ------
    TypeError
        If `value` was not given as `str` instance.
    """
    if value is None:
        return None
    
    if not isinstance(value, str):
        raise TypeError(f'`value` should be `str` instance, got {value.__class__.__name__}.')
    
    if not value:
        return ''
    
    value = value.encode('utf8')
    result = bytearray()
    percentage = None
    safe = f'{safe}{ALLOWED}{"" if query_string else QUERY_STRING_NOT_SAFE}{protected}'
    binary_safe = safe.encode('ascii')
    
    for char in value:
        if percentage is not None:
            if char in BIN_ASCII_LOWERCASE:
                char -= 32
            
            percentage.append(char)
            if len(percentage) == 3:
                percentage = bytes(percentage)
                try:
                    unquoted = chr(int(percentage[1:].decode('ascii'), base=16))
                except ValueError as err:
                    raise ValueError(f'Unallowed percentage: {percentage!r}.') from err
                
                if unquoted in protected:
                    result.extend(percentage)
                elif unquoted in safe:
                    result.append(ord(unquoted))
                else:
                    result.extend(percentage)
                
                percentage = None
            
            continue
            
        if char == b'%'[0]:
            percentage = bytearray()
            percentage.append(char)
            continue
        
        if query_string:
            if char == b' '[0]:
                result.append(b'+'[0])
                continue
        
        if char in binary_safe:
            result.append(char)
            continue
        
        result.extend((f'%{char:02X}').encode('ascii'))
    
    return result.decode('ascii')


def unquote(value, unsafe='', query_string=False):
    """
    Http quotes the given `value`.
    
    Parameters
    ----------
    value : `None` or `str`
        The value to quote.
    unsafe : `str`, Optional
        Additional not percentage encoding safe characters, which should not be contained by potentially percent
        encoded characters. Defaults to empty string.
    
    Returns
    -------
    unquoted : `None` or `str`
        The unquoted value. Returns `None` of `value` was given as `None` as well.
    
    Raises
    ------
    TypeError
        If `value` was not given neither as `None`, nor `str` instance.
    """
    if value is None:
        return None
    
    if not isinstance(value, str):
        raise TypeError(f'`value` can be `None` or `str` instance, got {value.__class__.__name__}.')
    
    if not value:
        return ''
    
    percentage = None
    last_percentage = ''
    percentages = bytearray()
    result = []
    
    for char in value:
        if (percentage is not None):
            percentage += char
            if len(percentage) == 3:
                percentages.append(int(percentage[1:], base=16))
                last_percentage = percentage
                percentage = None
            continue
        
        if percentages:
            try:
                unquoted = percentages.decode('utf8')
            except UnicodeDecodeError:
                pass
            else:
                if query_string and (unquoted in QUERY_STRING_NOT_SAFE):
                    result.append(quote(unquoted, query_string=True))
                elif unquoted in unsafe:
                    result.append(quote(unquoted))
                else:
                    result.append(unquoted)
                percentages.clear()
        
        if char == '%':
            percentage = char
            continue
        
        if percentages:
            result.append(last_percentage)  # %F8ab
            last_percentage = ''
        
        if char == '+':
            if char not in unsafe:
                char = ' '
            
            result.append(char)
            continue
        
        if char in unsafe:
            result.append('%')
            result.extend(ord(char).__format__('X'))
            continue
        
        result.append(char)
    
    if percentages:
        try:
            unquoted = percentages.decode('utf8')
        except UnicodeDecodeError:
            result.append(last_percentage)  # %F8
        else:
            if query_string and (unquoted in QUERY_STRING_NOT_SAFE):
                result.append(quote(unquoted, query_string=True))
            elif unquoted in unsafe:
                result.append(quote(unquoted))
            else:
                result.append(unquoted)
    
    return ''.join(result)
