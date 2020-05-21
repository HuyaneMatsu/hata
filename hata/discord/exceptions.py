# -*- coding: utf-8 -*-
__all__ = ('DiscordException', 'ERROR_CODES', 'IntentError', )

class DiscordException(Exception):
    """
    Represents an exception raised by Discord, when it respons with a not expected response code.
    
    Depending on Discord's reponse code, the http client's behaiours differently.
    
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
    | 429   | TOO MANY REQUESTS     | ratelimited   |
    +-------+-----------------------+---------------+
    | 500   | SERVER ERRROR         | \*retry       |
    +-------+-----------------------+---------------+
    | 502   | GATEWAY UNAVAILABLE   | \*retry       |
    +-------+-----------------------+---------------+
    | 5XX   | SERVER ERROR          | raise         |
    +-------+-----------------------+---------------+
    
    > \* For five times a request can fail with `OsError` or return `501` / `502` response code. If the request fails
    > with these cases for the fifth try and the last one resulted `501` or `502` response code, then
    > ``DiscordException`` will be raised.
    
    Attributes
    ----------
    response : ``ClientResponse``
        The http client reponse, what caused the error.
    data : `Any`
        Deserialized `json` response data if applicable.
    _messages : `None` or `list` of `str`
        Initally the `._messages` attribute is `None`, but when the `.messages` property is used for the first time,
        the messages will be parsed out from the resposne and from it's data.
    _code : `None` or `int`
        Initially the `._code` attribute is set to `None`, but first time when the `.code` property is accessed, it is
        parsed out. If the reponse data does not contains `code`, then this attribute is set to `0`.
    """
    def __init__(self, response, data):
        """
        Creates a new ``DiscordException``.
        
        Parameters
        ----------
        response : ``ClientResponse``
            The http client reponse, what caused the error.
        data : `Any`
            Deserialized `json` response data if applicable.
        """
        Exception.__init__(self)
        self.response=response
        self.data=data
        self._messages=None
        self._code=None
    
    @property
    def messages(self):
        """
        Returns a list of the errors. The 0th element of the list is always a header line, what contains the
        exception's name, the response's reason and it's status. If set, then also the Discord's internal error code
        and it's message as well.
        
        Every other element at the list is optional. Those are extra errors included in the reponse's data.
        
        Returns
        -------
        messages : `list` of `str`
        """
        messages=self._messages
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
        messages=[]
        code=self.code
        message_parts=[]
        data=self.data
        if type(data) is dict:
            message_base= data.get('message','')
            error_datas = data.get('errors')
            if error_datas:
                stack=[[(None,error_datas,)]]
                while True:
                    line=stack[-1]
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
                        
                        if message_parts[-1]!='.':
                            continue
                        
                        del message_parts[-1]
                        continue
                    
                    key,value=line[-1]
                    
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
                            error_datas=value['_errors']
                        except KeyError:
                            stack.append(list(value.items()))
                            continue
                        
                        for error_data in error_datas:
                            error_code=error_data.pop('code','ERROR')
                            error_message=error_data.pop('message','')
                            if error_data:
                                error_extra=' '.join(f'{key}={value!r}' for key,value in error_data.items())
                                if error_message:
                                    error_message=f'{error_message!r} {error_extra}'
                                else:
                                    error_message=error_extra
                            elif error_message:
                                error_message=repr(error_message)
                            
                            if message_parts:
                                message_parts.append('.')
                            
                            message_parts.append(f'{error_code}({error_message})')
                            messages.append(''.join(message_parts))
                            del message_parts[-1]
                            if not message_parts:
                                continue
                            
                            if message_parts[-1]!='.':
                                continue
                            
                            del message_parts[-1]
                            continue
                        
                        del line[-1]
                        if not message_parts:
                            continue
                            
                        del message_parts[-1]
                        
                        if not message_parts:
                            continue
                            
                        if message_parts[-1]!='.':
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
                    
                    if message_parts[-1]!='.':
                        continue
                    
                    del message_parts[-1]
                    
        else:
            message_base=''

        message_parts.append(f'{self.__class__.__name__} {self.response.reason} ({self.response.status})')
        
        if code:
            message_parts.append(f', code=')
            message_parts.append(code.__repr__())

        if message_base:
            message_parts.append(': ')
            message_parts.append(message_base)
        elif messages:
            message_parts.append(':')
        
        messages.append(''.join(message_parts))
        messages.reverse()
        
        self._messages=messages
        return messages
    
    def __repr__(self):
        """Returns the representation of the object."""
        return '\n'.join(self.messages)
    
    __str__=__repr__
    
    @property
    def code(self):
        """
        Returns the Discord's internal exception code, if it is included in the response's data. If not, then returns
        `0`.
        
        Returns
        -------
        error_code : `int`
        """
        code=self._code
        if code is None:
            code = self._cr_code()
        return code
    
    def _cr_code(self):
        """
        Parses out the Discord's inner exception code from the response's data. Sets it to `._code` and returns it as well.
        
        Returns
        -------
        error_code : `int`
        """
        data = self.data
        if type(data) is dict:
            code=data.get('code',0)
        else:
            code=0
        
        self._code=code
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


class ERROR_CODES:
    """
    Stores the possible json error codes received from Discord HTTP API requests.
    """
    unknown_account         = 10001
    unknown_application     = 10002
    unknown_channel         = 10003
    unknown_guild           = 10004
    unknown_integration     = 10005
    unknown_invite          = 10006
    unknown_member          = 10007
    unknown_message         = 10008
    unknown_overwrite       = 10009
    unknown_provider        = 10010
    unknown_role            = 10011
    unknown_token           = 10012
    unknown_user            = 10013
    unknown_emoji           = 10014
    unknown_webhook         = 10015
    unknown_ban             = 10026
    unknown_SKU             = 10027
    unknown_store_listing   = 10028
    unknown_entitlement     = 10029
    unknown_build           = 10030
    unknown_lobby           = 10031
    unknown_branch          = 10032
    unknown_redistributable = 10036
    
    bots_cannot_use_this_endpoint   = 20001
    only_bots_can_use_this_endpoint = 20002
    
    max_guilds              = 30001 # 100
    max_friends             = 30001 # 10000
    max_pins                = 30003 # 50
    max_roles               = 30005 # 250
    max_webhooks            = 30007 # 10
    max_reactions           = 30010 # 20
    max_channels            = 30013 # 500
    max_attachments         = 30015 # 10
    max_invites             = 30016 # 1000
    
    unauthorized            = 40001
    account_verification_neded = 40002
    request_too_large       = 40005
    feature_disabled        = 40006
    user_banned_from_guild  = 40007
    
    missing_access                  = 50001
    invalid_account_type            = 50002
    cannot_execute_action_in_dm     = 50003
    widget_disabled                 = 50004
    edit_other_users_message        = 50005
    empty_message                   = 50006
    cannot_send_message_to_user     = 50007
    cannot_send_message_to_voice_channel = 50008
    channel_verification_level_too_high = 50009
    oauth2_application_has_no_bot   = 50010
    oauth2_application_limit_reached= 50011
    oauth2_state_invalid            = 50012
    missing_permissions             = 50013
    invalid_auth_token              = 50014
    note_too_long                   = 50015
    invalid_amount_of_message_to_bulk_delete = 50016
    can_pin_message_at_its_own_channel = 50019
    invite_code_invalid_or_taken    = 50020
    cannot_execute_action_on_system_message = 50021
    cannot_execute_action_on_this_channel_type = 50024
    oauth2_access_token_invalid     = 50025
    invalid_recipients              = 50033
    message_too_old_to_bulk_delete  = 50034
    invalid_form_body               = 50035
    invite_accepted_where_application_bot_is_not_in = 50036
    invalid_API_version             = 50041
    
    reaction_blocked        = 90001
    
    resource_overloaded     = 130000

class IntentError(BaseException):
    """
    An intent error is raised by a ``DiscordGateway`` when a ``Client`` tries to log in with an invalid intent value.
    
    Attributes
    ----------
    code : `int`
        Gateway close code sent by Discord.
    
    Class Attributes
    ----------------
    CODETABLE : `dict` of (`int`, `str`) items
        A dictionary to store the descriptions for each intent related gateway close code.
    """
    CODETABLE = {
        4013 : 'An invalid intent is one that is not meaningful and not documented.',
        4014 : 'A disallowed intent is one which you have not enabled for your bot or one that your bot is not whitelisted to use.',
            }
    
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
        result = [
            self.__class__.__name__,
            '(code=',
                ]
        
        code = self.code
        result.append(repr(code))
        result.append(')')
        
        try:
            description = self.CODETABLE[code]
        except KeyError:
            pass
        else:
            result.append(': ')
            result.append(description)
        
        return ''.join(result)
