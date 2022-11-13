__all__ = ('DiscordException',)

import re

from scarletio.web_common.headers import DATE, RETRY_AFTER

from ...env import RICH_DISCORD_EXCEPTION

from ..utils import DATETIME_FORMAT_CODE, parse_date_header_to_datetime


if RICH_DISCORD_EXCEPTION:
    from .payload_renderer import reconstruct_payload
else:
    reconstruct_payload = None

EXCEPTION_RESPONSE_RP = re.compile('\d+\: (.*)')


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
    with these cases for the fifth try and the last one resulted `501` / `502` response code, then
    ``DiscordException`` will be raised.
    
    Attributes
    ----------
    debug_options : `None`, `tuple` of `str`
        Debug options of the http client.
    
    received_data : `Any`
        Deserialized `json` response data if applicable.
    
    response : ``ClientResponse``
        The http client response, what caused the error.
    
    sent_data : `ANy`
        Sent data.
    
    _code : `None`, `int`
        Cache of the `.code` property.
        
        If the response data does not contains `code`, then this attribute is set to `0`.
    
    _debug_info : `None`, `str`
        cache of the `.debug_info` property.
    
    _errors : `None`, `list` of `str`
        Cache of the `errors` property.
    
    _request_info : `None`, `str`
        Cache of the `.request_info` property.
    
    _message : `None`,  `str`
        Cache of the `.message` property.
    """
    def __init__(self, response, received_data, sent_data, debug_options):
        """
        Creates a new ``DiscordException``.
        
        Parameters
        ----------
        response : ``ClientResponse``
            The http client response, what caused the error.
        received_data : `Any`
            Deserialized `json` response data if applicable.
        sent_data : `Any`
            Sent data.
        debug_options : `None`, `tuple` of `str`
            Debug options of the http client.
        """
        Exception.__init__(self)
        self.response = response
        self.received_data = received_data
        self.sent_data = sent_data
        self.debug_options = debug_options
        self._code = None
        self._debug_info = None
        self._errors = None
        self._request_info = None
        self._message = None
    
    
    @property
    def message(self):
        """
        Returns the error message of the discord exception.
        
        Returns
        -------
        message : `str`
        """
        message = self._message
        if message is None:
            message = self._create_message()
            self._message = message
        
        return message
    
    
    def _create_message(self):
        """
        Creates the error message of the discord exception.
        
        Returns
        -------
        message : `str`
        """
        message_parts = []
        
        message_parts.append(self.__class__.__name__)
        message_parts.append(' ')
        response = self.response
        message_parts.append(response.reason)
        message_parts.append(' (')
        message_parts.append(repr(response.status))
        message_parts.append(')')
        
        code = self.code
        if code:
            message_parts.append(f', code=')
            message_parts.append(repr(code))
        
        received_data = self.received_data
        if isinstance(received_data, dict):
            message_base = received_data.get('message', '')
        else:
            message_base = ''
        
        if message_base:
            # At some cases we might get message like `400: text` At this case want to cut the status part.
            matched = EXCEPTION_RESPONSE_RP.fullmatch(message_base)
            if (matched is not None):
                message_base = matched.group(1)
            
            message_parts.append(': ')
            message_parts.append(message_base)
        
        
        if response.status == 429:
            if not message_base.endswith(('.', ',')):
                message_parts.append(';')
            
            message_parts.append('retry after: ')
            message_parts.append(format(self.retry_after, '.02f'))
        
        return ''.join(message_parts)
    
    
    @property
    def request_info(self):
        """
        Returns additional request information about the exception.
        
        Returns
        -------
        request_info : `str`
        """
        request_info = self._request_info
        if request_info is None:
            request_info = self._create_request_info()
            self._request_info = request_info
        
        return request_info
    
    
    def _create_request_info(self):
        """
        Creates additional request information about the exception.
        
        Returns
        -------
        request_info : `str`
        """
        response = self.response
        message_parts = []
        
        message_parts.append(format(parse_date_header_to_datetime(response.headers[DATE]), DATETIME_FORMAT_CODE))
        message_parts.append('; ')
        message_parts.append(response.method)
        message_parts.append(' ')
        message_parts.append(str(response.url))
        
        return ''.join(message_parts)
    
    
    @property
    def errors(self):
        """
        Returns the errors shipped with the exception.
        
        Might return an empty list.
        
        Returns
        -------
        errors : `list` of `str`
        """
        errors = self._errors
        if errors is None:
            errors = self._create_errors()
            self._errors = errors
        
        return errors
    
    
    def _create_errors(self):
        """
        Creates the errors shipped with the exception.
        
        Might return an empty list.
        
        Returns
        -------
        errors : `list` of `str`
        """
        messages = []
        
        message_parts = []
        received_data = self.received_data
        if isinstance(received_data, dict):
            error_datas = received_data.get('errors', None)
            if (error_datas is not None) and error_datas:
                stack = [[(None, error_datas)]]
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
                    
                    if isinstance(value, dict):
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
                            stack.append([*value.items()])
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
        
        messages.reverse()
        return messages
    
    
    @property
    def debug_info(self):
        """
        Returns debug info.
        
        Only displayed within `.messages` when rich discord exceptions are enabled.
        
        Returns
        -------
        debug_info : `str`
        """
        
        debug_info = self._debug_info
        if debug_info is None:
            debug_info = self._create_debug_info()
            self._debug_info = debug_info
        
        return debug_info
    
    
    def _create_debug_info(self):
        """
        Creates debug info.
        
        Returns
        -------
        debug_info : `str`
        """
        debug_options = self.debug_options
        if (debug_options is None):
            return ''
        
        debug_info_parts = ['debug options: ']
        
        index = 0
        limit = len(debug_options)
        while True:
            debug_option = debug_options[index]
            index += 1
            
            debug_info_parts.append(debug_option)
            
            if index == limit:
                break
            
            debug_info_parts.append(', ')
            continue
        
        return ''.join(debug_info_parts)
    
    
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
        messages = []
        
        messages.append(self.message)
        messages.append(self.request_info)
        
        messages.extend(self.errors)
        
        if RICH_DISCORD_EXCEPTION:
            debug_info = self.debug_info
            if debug_info:
                messages.append(debug_info)
            
            reconstructed_payload = reconstruct_payload(self.sent_data)
            if (reconstructed_payload is not None):
                messages.append(reconstructed_payload)
        
        return messages
    
    
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
            code = self._get_code()
            self._code = code
        
        return code
    
    
    def _get_code(self):
        """
        Parses out the Discord's inner exception code from the response's data. Sets it to `._code` and returns it as
        well.
        
        Returns
        -------
        error_code : `int`
        """
        received_data = self.received_data
        if isinstance(received_data, dict):
            code = received_data.get('code', 0)
        else:
            code = 0
        
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
    
    
    @property
    def retry_after(self):
        """
        After how much seconds the request should be retried.
        Applicable for rate limit errors, so the ones with status `429`.
        
        Returns
        -------
        retry_after : `float`
        """
        try:
            retry_after = self.response.headers[RETRY_AFTER]
        except KeyError:
            return 0.0
        
        try:
            retry_after = float(retry_after)
        except ValueError:
            return 0.0
        
        return retry_after
    
    
    def __repr__(self):
        """Returns the representation of the object."""
        return '\n'.join(self.messages)
    
    
    __str__ = __repr__
    
    def __format__(self, code):
        """
        Formats the discord exception in a format string.
        
        The only provided option is no code, which returns a short-ish representation.
        
        Parameters
        ----------
        code : `str`
            The option on based the result will be formatted.
        
        Returns
        -------
        exception : `str`
        
        Raises
        ------
        ValueError
            Unknown format code.
        """
        if not code:
            return f'<{self.message}>'
        
        raise ValueError(
            f'Unknown format code {code!r} for {self.__class__.__name__}; {self!r}. '
            f'Available format codes: {""!r}.'
        )
