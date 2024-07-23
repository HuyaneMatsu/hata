__all__ = ('DiscordException',)

import re

from scarletio.web_common.headers import DATE, RETRY_AFTER

from ...env import RICH_DISCORD_EXCEPTION

from ..utils import DATETIME_FORMAT_CODE, parse_date_header_to_datetime


if RICH_DISCORD_EXCEPTION:
    from .payload_renderer import reconstruct_payload
else:
    reconstruct_payload = None


EXCEPTION_RESPONSE_RP = re.compile('\\d+\\: (.*)')


class DiscordException(Exception):
    r"""
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
    _code : `None`, `int`
        Cache of the `.code` property.
        
        If the response data does not contains `code`, then this attribute is set to `0`.
    
    _debug_info : `None`, `str`
        cache of the `.debug_info` property.
    
    _errors : `None`, `list` of `str`
        Cache of the `errors` property.
    
    _request_info : `None`, `str`
        Cache of the `.request_info` property.
    
    _retry_after : `None`, `float`
        Cache pf the `.retry_after` property.
    
    _message : `None`,  `str`
        Cache of the `.message` property.
    
    _status : `None`, `int`
        Cache of the `.status` property.
    
    debug_options : `None`, `set` of `str`
        Debug options of the http client.
    
    received_data : `object`
        Deserialized `json` response data if applicable.
    
    response : ``ClientResponse``
        The http client response, what caused the error.
    
    sent_data : `object`
        Sent data.
    """
    __slots__ = (
        '_code', '_debug_info', '_errors', '_request_info', '_retry_after', '_message', '_status', 'debug_options',
        'received_data', 'response', 'sent_data',
    )
    
    def __new__(cls, response, received_data, sent_data, debug_options):
        """
        Creates a new discord exception.
        
        Parameters
        ----------
        response : `None | ClientResponse`
            The http client response, what caused the error.
        received_data : `object`
            Deserialized `json` response data if applicable.
        sent_data : `object`
            Sent data.
        debug_options : `None`, `set` of `str`
            Debug options of the http client.
        """
        self = Exception.__new__(cls, response, received_data, sent_data, debug_options)
        self._code = None
        self._debug_info = None
        self._errors = None
        self._request_info = None
        self._retry_after = None
        self._message = None
        self._status = None
        self.debug_options = debug_options
        self.received_data = received_data
        self.response = response
        self.sent_data = sent_data
        return self
    
    
    __init__ = object.__init__
    
    
    def _get_message(self):
        """
        Creates the error message of the discord exception.
        
        Returns
        -------
        message : `str`
        """
        message_parts = []
        
        message_parts.append(type(self).__name__)
        response = self.response
        if (response is not None):
            message_parts.append(' ')
            message_parts.append(response.reason)
            message_parts.append(' (')
            message_parts.append(repr(response.status))
            message_parts.append(')')
        
        code = self.code
        if code:
            message_parts.append(', code = ')
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
        
        
        if self.status == 429:
            if not message_base.endswith(('.', ',')):
                message_parts.append(';')
            
            message_parts.append(' retry after: ')
            message_parts.append(format(self.retry_after, '.02f'))
        
        return ''.join(message_parts)
    
    
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
            message = self._get_message()
            self._message = message
        
        return message
    
    
    @message.setter
    def message(self, value):
        self._message = value
    
    
    @message.deleter
    def message(self):
        self._message = None
    
    
    def _get_request_info(self):
        """
        Creates additional request information about the exception.
        
        Returns
        -------
        request_info : `str`
        """
        response = self.response
        if response is None:
            return ''
        
        message_parts = []
        
        message_parts.append(format(parse_date_header_to_datetime(response.headers[DATE]), DATETIME_FORMAT_CODE))
        message_parts.append('; ')
        message_parts.append(response.method)
        message_parts.append(' ')
        message_parts.append(str(response.url))
        
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
            request_info = self._get_request_info()
            self._request_info = request_info
        
        return request_info
    
    
    @request_info.setter
    def request_info(self, value):
        self._request_info = value
    
    
    @request_info.deleter
    def request_info(self):
        self._request_info = None
    
    
    def _get_errors(self):
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
                                    f'{key} = {value!r}' for key, value in error_data.items()
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
            errors = self._get_errors()
            self._errors = errors
        
        return errors
    
    
    @errors.setter
    def errors(self, value):
        self._errors = value
    
    
    @errors.deleter
    def errors(self):
        self._errors = None
    
    
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
        
        debug_options = sorted(debug_options)
        
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
    
    
    @debug_info.setter
    def debug_info(self, value):
        self._debug_info = value
    
    
    @debug_info.deleter
    def debug_info(self):
        self._debug_info = None
    
    
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
    
    
    @messages.setter
    def messages(self, value):
        self._messages = value
    
    
    @messages.deleter
    def messages(self):
        self._messages = None
    
    
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
    
    
    @code.setter
    def code(self, value):
        self._code = value
    
    
    @code.deleter
    def code(self):
        self._code = None
    
    
    def _get_status(self):
        """
        Returns the response's status. Defaults to `0`.
        
        Returns
        -------
        status : `int`
        """
        response = self.response
        if (response is None):
            return 0
        
        return response.status
        
    
    @property
    def status(self):
        """
        The exception's response's status.
        
        Returns
        -------
        status : `int`
        """
        status = self._status
        if status is None:
            status = self._get_status()
            self._status = status
        
        return status
    
    
    @status.setter
    def status(self, value):
        self._status = value
    
    
    @status.deleter
    def status(self):
        self._status = None
    
    
    def _get_retry_after(self):
        """
        Returns after how much seconds the request should be retried. Defaults to `0.0`.
        
        Returns
        -------
        retry_after : `float`
        """
        response = self.response
        if response is None:
            return 0.0
        
        try:
            retry_after = response.headers[RETRY_AFTER]
        except KeyError:
            return 0.0
        
        try:
            retry_after = float(retry_after)
        except ValueError:
            return 0.0
        
        return retry_after
    
    
    @property
    def retry_after(self):
        """
        After how much seconds the request should be retried.
        Applicable for rate limit errors, so the ones with status `429`.
        
        Returns
        -------
        retry_after : `float`
        """
        retry_after = self._retry_after
        if retry_after is None:
            retry_after = self._get_retry_after()
            self._retry_after = retry_after
        
        return retry_after
    
    
    @retry_after.setter
    def retry_after(self, value):
        self._retry_after = value
    
    
    @retry_after.deleter
    def retry_after(self):
        self._retry_after = None
    
    
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
