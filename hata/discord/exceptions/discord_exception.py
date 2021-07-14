__all__ = ('DiscordException',)


from ...backend.headers import RETRY_AFTER, DATE

from ..utils import parse_date_header_to_datetime, DATETIME_FORMAT_CODE

class DiscordException(Exception):
    """
    Represents an exception raised by Discord, when it response with a not expected response code.
    
    Depending on Discord's response code, the http client's behaviours differently.
    
    +-------+-----------------------+---------------+
    | Code  | Meaning               | Behaviour     |
    +=======+=======================+===============+
    | 200   | OK                    | return        |
    +-------+-----------------------+---------------+
    | 201   | CREATED               | return        |
    +-------+-----------------------+---------------+
    | 204   | NO CONTENT            | return        |
    +-------+-----------------------+---------------+
    | 304   | NOT MODIFIED          | return        |
    +-------+-----------------------+---------------+
    | 400   | BAD REQUEST           | raise         |
    +-------+-----------------------+---------------+
    | 401   | UNAUTHORIZED          | raise         |
    +-------+-----------------------+---------------+
    | 403   | FORBIDDEN             | raise         |
    +-------+-----------------------+---------------+
    | 404   | NOT FOUND             | raise         |
    +-------+-----------------------+---------------+
    | 405   | METHOD NOT ALLOWED    | raise         |
    +-------+-----------------------+---------------+
    | 429   | TOO MANY REQUESTS     | rate limited  |
    +-------+-----------------------+---------------+
    | 500   | SERVER ERROR          | \*retry       |
    +-------+-----------------------+---------------+
    | 502   | GATEWAY UNAVAILABLE   | \*retry       |
    +-------+-----------------------+---------------+
    | 5XX   | SERVER ERROR          | raise         |
    +-------+-----------------------+---------------+
    
    \* For five times a request can fail with `OsError` or return `501` / `502` response code. If the request fails
    with these cases for the fifth try and the last one resulted `501` or `502` response code, then
    ``DiscordException`` will be raised.
    
    Attributes
    ----------
    response : ``ClientResponse``
        The http client response, what caused the error.
    data : `Any`
        Deserialized `json` response data if applicable.
    _messages : `None` or `list` of `str`
        Initially the `._messages` attribute is `None`, but when the `.messages` property is used for the first time,
        the messages will be parsed out from the response and from it's data.
    _code : `None` or `int`
        Initially the `._code` attribute is set to `None`, but first time when the `.code` property is accessed, it is
        parsed out. If the response data does not contains `code`, then this attribute is set to `0`.
    """
    def __init__(self, response, data):
        """
        Creates a new ``DiscordException``.
        
        Parameters
        ----------
        response : ``ClientResponse``
            The http client response, what caused the error.
        data : `Any`
            Deserialized `json` response data if applicable.
        """
        Exception.__init__(self)
        self.response = response
        self.data = data
        self._messages = None
        self._code = None
    
    @property
    def messages(self):
        """
        Returns a list of the errors. The 0th element of the list is always a header line, what contains the
        exception's name, the response's reason and it's status. If set, then also the Discord's internal error code
        and it's message as well.
        
        Every other element at the list is optional. Those are extra errors included in the response's data.
        
        Returns
        -------
        messages : `list` of `str`
        """
        messages = self._messages
        if messages is None:
            messages = self._cr_messages()
        return messages
    
    def _cr_messages(self):
        """
        Generates the exception's messages from the causer response's headers. If the response's data contains `code`
        or / and `message` as well, then it will complement the exception message's header line with those too.
        
        If the response's data contains additional errors too, then those will be parsed out, and added to the list.
        
        Saves the result to the `._messages` instance attribute and saves it as well.
        
        Returns
        -------
        messages : `list` of `str`
        """
        messages = []
        
        message_parts = []
        data = self.data
        if type(data) is dict:
            message_base = data.get('message', '')
            error_datas = data.get('errors', None)
            if (error_datas is not None) and error_datas:
                stack = [[(None, error_datas,)]]
                while True:
                    line = stack[-1]
                    if not line:
                        del stack[-1]
                        if not stack:
                            break
                            
                        del stack[-1][-1]
                        if not message_parts:
                            continue
                            
                        del message_parts[-1]
                        if not message_parts:
                            continue
                        
                        if message_parts[-1] != '.':
                            continue
                        
                        del message_parts[-1]
                        continue
                    
                    key, value = line[-1]
                    
                    if type(value) is dict:
                        if (key is not None):
                            if key.isdigit():
                                # this should not be first ever
                                message_parts.append(f'[{key}]')
                            else:
                                if message_parts:
                                    message_parts.append('.')
                                message_parts.append(key)
                        try:
                            error_datas = value['_errors']
                        except KeyError:
                            stack.append(list(value.items()))
                            continue
                        
                        for error_data in error_datas:
                            error_data_length = len(error_data)
                            try:
                                error_code = error_data['code']
                            except KeyError:
                                error_code = 'ERROR'
                            else:
                                error_data_length -= 1
                            
                            try:
                                error_message = error_data['message']
                            except KeyError:
                                error_message = None
                            else:
                                error_data_length -= 1
                            
                            if error_data_length:
                                error_extra = ' '.join(
                                    f'{key}={value!r}' for key, value in error_data.items()
                                        if key not in ('code', 'message')
                                )
                                
                                if (error_message is None):
                                    error_message = error_extra
                                else:
                                    error_message = f'{error_message!r} {error_extra}'
                            
                            elif (error_message is None):
                                error_message = ''
                            else:
                                error_message = repr(error_message)
                            
                            if message_parts:
                                message_parts.append('.')
                            
                            message_parts.append(f'{error_code}({error_message})')
                            messages.append(''.join(message_parts))
                            del message_parts[-1]
                            if not message_parts:
                                continue
                            
                            if message_parts[-1] != '.':
                                continue
                            
                            del message_parts[-1]
                            continue
                        
                        del line[-1]
                        if not message_parts:
                            continue
                            
                        del message_parts[-1]
                        
                        if not message_parts:
                            continue
                            
                        if message_parts[-1] != '.':
                            continue
                        
                        del message_parts[-1]
                        continue
                    
                    if key.isdigit():
                        message_parts.append(f'[{key}]')
                    else:
                        message_parts.append('.')
                        message_parts.append(key)
                    message_parts.append('.')
                    message_parts.append(value)
                    messages.append(''.join(message_parts))
                    del line[-1]
                    del message_parts[-3:]
                    if not message_parts:
                        continue
                    
                    if message_parts[-1] != '.':
                        continue
                    
                    del message_parts[-1]
                    
        else:
            message_base = ''
        
        response = self.response
        message_parts.append(parse_date_header_to_datetime(response.headers[DATE]).__format__(DATETIME_FORMAT_CODE))
        message_parts.append('; ')
        message_parts.append(response.method)
        message_parts.append(' ')
        message_parts.append(str(response.url))
        messages.append(''.join(message_parts))
        
        message_parts.clear()
        
        message_parts.append(f'{self.__class__.__name__} {response.reason} ({response.status})')
        
        code = self.code
        if code:
            message_parts.append(f', code=')
            message_parts.append(repr(code))

        if message_base:
            message_parts.append(': ')
            message_parts.append(message_base)
        elif messages:
            message_parts.append(':')
        
        messages.append(''.join(message_parts))
        messages.reverse()
        
        if self.response.status == 429:
            try:
                retry_after = self.response.headers[RETRY_AFTER]
            except KeyError:
                pass
            else:
                messages.append(f'{RETRY_AFTER}: {retry_after}')
        
        self._messages = messages
        return messages
    
    def __repr__(self):
        """Returns the representation of the object."""
        return '\n'.join(self.messages)
    
    __str__ = __repr__
    
    @property
    def code(self):
        """
        Returns the Discord's internal exception code, if it is included in the response's data. If not, then returns
        `0`.
        
        Returns
        -------
        error_code : `int`
        """
        code = self._code
        if code is None:
            code = self._cr_code()
        return code
    
    def _cr_code(self):
        """
        Parses out the Discord's inner exception code from the response's data. Sets it to `._code` and returns it as
        well.
        
        Returns
        -------
        error_code : `int`
        """
        data = self.data
        if type(data) is dict:
            code = data.get('code', 0)
        else:
            code = 0
        
        self._code = code
        return code
    
    @property
    def status(self):
        """
        The exception's response's status.
        
        Returns
        -------
        status_code : `int`
        """
        return self.response.status
