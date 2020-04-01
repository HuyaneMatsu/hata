# -*- coding: utf-8 -*-
#https://github.com/squeaky-pl/zenchmarks/blob/master/vendor/yarl/quoting.py
from string import ascii_letters, ascii_lowercase, digits

BASCII_LOWERCASE    = ascii_lowercase.encode('ascii')
BPCT_ALLOWED        = {f'%{i:02X}'.encode('ascii') for i in range(256)}
GEN_DELIMS          = ':/?#[]@'
SUB_DELIMS_WO_QS    = '!$\'()*,'
SUB_DELIMS          = f'{SUB_DELIMS_WO_QS}+&=;'
RESERVED            = f'{GEN_DELIMS}{SUB_DELIMS}'
UNRESERVED          = f'{ascii_letters}{digits}-._~'
ALLOWED             = f'{UNRESERVED}{SUB_DELIMS_WO_QS}'


def quote(value,safe='',protected='',qs=False):
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError("Argument should be str")
    if not value:
        return ''
    value   = value.encode('utf8')
    result  = bytearray()
    pct     = b''
    if qs:
        safe=f'{safe}{ALLOWED}{protected}'
    else:
        safe=f'{safe}{ALLOWED}+&={protected}'
    bsafe   =safe.encode('ascii')
    
    for char in value:
        if pct:
            if char in BASCII_LOWERCASE:
                char=char-32
            pct.append(char)
            if len(pct)==3:  # pragma: no branch   # peephole optimizer
                pct=bytes(pct)
                try:
                    unquoted=chr(int(pct[1:].decode('ascii'),base=16))
                except ValueError:
                    raise ValueError(f'Unallowed PCT {pct}')
                if unquoted in protected:
                    result.extend(pct)
                elif unquoted in safe:
                    result.append(ord(unquoted))
                else:
                    result.extend(pct)
                pct=b''
            continue
        elif char==ord('%'):
            pct=bytearray()
            pct.append(char)
            continue

        if qs:
            if char==ord(' '):
                result.append(ord('+'))
                continue
        if char in bsafe:
            result.append(char)
            continue

        result.extend((f'%{char:02X}').encode('ascii'))

    return result.decode('ascii')


def unquote(value,unsafe='',qs=False):
    if value is None:
        return None
    if not isinstance(value,str):
        raise TypeError('Argument should be str')
    if not value:
        return ''
    
    pct     = ''
    last_pct= ''
    pcts    = bytearray()
    result  = []
    
    for char in value:
        if pct:
            pct+=char
            if len(pct)==3:  # peephole optimizer
                pcts.append(int(pct[1:],base=16))
                last_pct=pct
                pct=''
            continue
        if pcts:
            try:
                unquoted=pcts.decode('utf8')
            except UnicodeDecodeError:
                pass
            else:
                if qs and unquoted in '+=&':
                    result.append(quote(unquoted,qs=True))
                elif unquoted in unsafe:
                    result.append(quote(unquoted))
                else:
                    result.append(unquoted)
                del pcts[:]

        if char=='%':
            pct=char
            continue

        if pcts:
            result.append(last_pct)  # %F8ab
            last_pct=''

        if char=='+':
            if char in unsafe:
                result.append('+')
            else:
                result.append(' ')
            continue

        if char in unsafe:
            result.append('%')
            h=hex(ord(char)).upper()[2:]
            for char in h:
                result.append(char)
            continue

        result.append(char)

    if pcts:
        try:
            unquoted = pcts.decode('utf8')
        except UnicodeDecodeError:
            result.append(last_pct)  # %F8
        else:
            if qs and unquoted in '+=&':
                result.append(quote(unquoted, qs=True))
            elif unquoted in unsafe:
                result.append(quote(unquoted))
            else:
                result.append(unquoted)
    return ''.join(result)
