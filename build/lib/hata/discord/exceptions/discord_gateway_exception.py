__all__ = ('DiscordGatewayException', 'GATEWAY_EXCEPTION_CODE_TABLE', 'INTENT_ERROR_CODES', 'RESHARD_ERROR_CODES')

INTENT_ERROR_CODES = frozenset((4013, 4014,))
RESHARD_ERROR_CODES = frozenset((4011,))

GATEWAY_EXCEPTION_CODE_TABLE = {
    4011: 'A gateway would have handled too many guilds, resharding is required.',
    4013: 'An invalid intent is one that is not meaningful and not documented.',
    4014: 'A disallowed intent is one which you have not enabled for your bot or one that your bot is not '
          'whitelisted to use.',
}

"""
GATEWAY_EXCEPTION_CODE_TABLE : `dict` of (`int`, `str`) items
    A dictionary to store the descriptions for each gateway close code.
INTENT_ERROR_CODES : `frozenset` of `int` = (`4013`, `4014`)
    Close codes of intent errors.
RESHARD_ERROR_CODES : `frozenset` of `int` = (`4011`,)
    Error codes when resharding is required.
"""

class DiscordGatewayException(BaseException):
    """
    An intent error is raised by a ``DiscordGateway`` when a ``Client`` tries to log in with an invalid intent value.
    
    Attributes
    ----------
    code : `int`
        Gateway close code sent by Discord.
    """
    def __init__(self, code):
        """
        Creates an intent error with the related gateway close error code.
        
        Parameters
        ----------
        code : `int`
            Gateway close code.
        """
        BaseException.__init__(self, code)
        self.code = code
    
    def __repr__(self):
        """Returns the representation of the intent error."""
        repr_parts = [
            self.__class__.__name__,
            '(code=',
        ]
        
        code = self.code
        repr_parts.append(repr(code))
        repr_parts.append(')')
        
        try:
            description = GATEWAY_EXCEPTION_CODE_TABLE[code]
        except KeyError:
            pass
        else:
            repr_parts.append(': ')
            repr_parts.append(description)
        
        return ''.join(repr_parts)
