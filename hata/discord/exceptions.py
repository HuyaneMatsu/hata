# -*- coding: utf-8 -*-
__all__ = ('DiscordException', 'DiscordGatewayException', 'ERROR_CODES', 'InvalidToken',)

from ..backend.headers import RETRY_AFTER

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
        code = self.code
        message_parts = []
        data = self.data
        if type(data) is dict:
            message_base = data.get('message', '')
            error_datas = data.get('errors')
            if error_datas:
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
                            error_code = error_data.pop('code', 'ERROR')
                            error_message = error_data.pop('message', '')
                            if error_data:
                                error_extra = ' '.join(f'{key}={value!r}' for key, value in error_data.items())
                                if error_message:
                                    error_message = f'{error_message!r} {error_extra}'
                                else:
                                    error_message = error_extra
                            elif error_message:
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
        
        message_parts.append(f'{self.__class__.__name__} {self.response.reason} ({self.response.status})')
        
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


class ERROR_CODES:
    """
    Stores the possible json error codes received from Discord HTTP API requests.
    
    These are the following:
    
    +---------------------------------------------------+-----------+-------+
    | Respective name                                   | Value     | Notes |
    +===================================================+===========+=======+
    | unknown_account                                   | 10001     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_application                               | 10002     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_channel                                   | 10003     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_guild                                     | 10004     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_integration                               | 10005     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_invite                                    | 10006     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_member                                    | 10007     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_message                                   | 10008     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_overwrite                                 | 10009     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_provider                                  | 10010     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_role                                      | 10011     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_token                                     | 10012     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_user                                      | 10013     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_emoji                                     | 10014     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_webhook                                   | 10015     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_webhook_service                           | 10016     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_ban                                       | 10026     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_SKU                                       | 10027     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_store_listing                             | 10028     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_entitlement                               | 10029     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_build                                     | 10030     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_lobby                                     | 10031     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_branch                                    | 10032     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_redistributable                           | 10036     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_gift_code                                 | 10038     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_guild_template                            | 10057     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_discovery_category                        | 10059     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_interaction                               | 10062     | -     |
    +---------------------------------------------------+-----------+-------+
    | unknown_application_command                       | 10063     | -     |
    +---------------------------------------------------+-----------+-------+
    | bots_not_allowed                                  | 20001     | -     |
    +---------------------------------------------------+-----------+-------+
    | only_bots_allowed                                 | 20002     | -     |
    +---------------------------------------------------+-----------+-------+
    | RPC_proxy_disallowed                              | 20003     | -     |
    +---------------------------------------------------+-----------+-------+
    | explicit_content                                  | 20009     | -     |
    +---------------------------------------------------+-----------+-------+
    | account_scheduled_for_deletion                    | 20011     | -     |
    +---------------------------------------------------+-----------+-------+
    | user_not_authorized_for_application               | 20012     | -     |
    +---------------------------------------------------+-----------+-------+
    | account_disabled                                  | 20013     | -     |
    +---------------------------------------------------+-----------+-------+
    | slowmode_rate_limited                             | 20016     | -     |
    +---------------------------------------------------+-----------+-------+
    | channel_following_edit_rate_limited               | 20022     | -     |
    +---------------------------------------------------+-----------+-------+
    | under_minimum_age                                 | 20024     | -     |
    +---------------------------------------------------+-----------+-------+
    | channel_send_rate_limit                           | 20028     | -     |
    +---------------------------------------------------+-----------+-------+
    | max_guilds                                        | 30001     | 100   |
    +---------------------------------------------------+-----------+-------+
    | max_friends                                       | 30001     | 10000 |
    +---------------------------------------------------+-----------+-------+
    | max_pins                                          | 30003     | 50    |
    +---------------------------------------------------+-----------+-------+
    | max_recipients                                    | 30004     | -     |
    +---------------------------------------------------+-----------+-------+
    | max_roles                                         | 30005     | 250   |
    +---------------------------------------------------+-----------+-------+
    | max_used_usernames                                | 30006     | -     |
    +---------------------------------------------------+-----------+-------+
    | max_webhooks                                      | 30007     | 10    |
    +---------------------------------------------------+-----------+-------+
    | max_emoji                                         | 30008     | -     |
    +---------------------------------------------------+-----------+-------+
    | max_reactions                                     | 30010     | 20    |
    +---------------------------------------------------+-----------+-------+
    | max_channels                                      | 30013     | 500   |
    +---------------------------------------------------+-----------+-------+
    | max_attachments                                   | 30015     | 10    |
    +---------------------------------------------------+-----------+-------+
    | max_invites                                       | 30016     | 1000  |
    +---------------------------------------------------+-----------+-------+
    | max_animated_emoji                                | 30018     | -     |
    +---------------------------------------------------+-----------+-------+
    | not_enough_guild_members                          | 30029     | -     |
    +---------------------------------------------------+-----------+-------+
    | max_guild_discovery_category                      | 30030     | 5     |
    +---------------------------------------------------+-----------+-------+
    | unauthorized                                      | 40001     | -     |
    +---------------------------------------------------+-----------+-------+
    | email_verification_required                       | 40002     | -     |
    +---------------------------------------------------+-----------+-------+
    | rate_limit_DM_open                                | 40003     | -     |
    +---------------------------------------------------+-----------+-------+
    | send_message_temporarily_disabled                 | 40004     | -     |
    +---------------------------------------------------+-----------+-------+
    | request_too_large                                 | 40005     | -     |
    +---------------------------------------------------+-----------+-------+
    | feature_disabled                                  | 40006     | -     |
    +---------------------------------------------------+-----------+-------+
    | user_banned                                       | 40007     | -     |
    +---------------------------------------------------+-----------+-------+
    | connection_rewoked                                | 40012     | -     |
    +---------------------------------------------------+-----------+-------+
    | delete_account_transfer_team_ownership            | 40028     | -     |
    +---------------------------------------------------+-----------+-------+
    | user_not_connected                                | 40032     | -     |
    +---------------------------------------------------+-----------+-------+
    | message_already_crossposted                       | 40033     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_access                                    | 50001     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_account_type                              | 50002     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_action_DM                                 | 50003     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_widget_disabled                           | 50004     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_message_author                            | 50005     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_message_empty                             | 50006     | -     |
    +---------------------------------------------------+-----------+-------+
    | cannot_message_user                               | 50007     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_message_send_non_text                     | 50008     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_message_verification_level                | 50009     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_oauth_app_bot                             | 50010     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_oauth_app_limit                           | 50011     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_oauth_state                               | 50012     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_permissions                               | 50013     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_token                                     | 50014     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_note                                      | 50015     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_bulk_delete_count                         | 50016     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_MFA_level                                 | 50017     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_password                                  | 50018     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_pin_message_channel                       | 50019     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_or_taken_invite_code                      | 50020     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_message_system                            | 50021     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_phone_number                              | 50022     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_client_id                                 | 50023     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_channel_type                              | 50024     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_oauth2_access_token                       | 50025     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_oauth2_missing_scope                      | 50026     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_webhook_token                             | 50027     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_recipients                                | 50033     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_bulk_delete_message_age                   | 50034     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_form_body                                 | 50035     | -     |
    +---------------------------------------------------+-----------+-------+
    | cannot_add_user_to_guild_where_bot_is_not         | 50036     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_sticker_sent                              | 50081     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_API_version                               | 50041     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_gift_redemption_exhausted                 | 50050     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_gift_redemption_owned                     | 50051     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_gift_self_redemption                      | 50054     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_message_type                              | 50068     | -     |
    +---------------------------------------------------+-----------+-------+
    | cannot_delete_community_channel                   | 50074     | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_gift_redemption_subscription_managed      | 100021    | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_gift_redemption_subscription_incompatible | 100023    | -     |
    +---------------------------------------------------+-----------+-------+
    | invalid_gift_redemption_invoice_open              | 100024    | -     |
    +---------------------------------------------------+-----------+-------+
    | MFA_enabled                                       | 60001     | -     |
    +---------------------------------------------------+-----------+-------+
    | MFA_disabled                                      | 60002     | -     |
    +---------------------------------------------------+-----------+-------+
    | MFA_required                                      | 60003     | -     |
    +---------------------------------------------------+-----------+-------+
    | MFA_unverified                                    | 60004     | -     |
    +---------------------------------------------------+-----------+-------+
    | MFA_invalid_secret                                | 60005     | -     |
    +---------------------------------------------------+-----------+-------+
    | MFA_invalid_ticket                                | 60006     | -     |
    +---------------------------------------------------+-----------+-------+
    | MFA_invalid_code                                  | 60008     | -     |
    +---------------------------------------------------+-----------+-------+
    | MFA_invalid_session                               | 60009     | -     |
    +---------------------------------------------------+-----------+-------+
    | phone_number_unable_to_send                       | 70003     | -     |
    +---------------------------------------------------+-----------+-------+
    | relationship_incoming_disabled                    | 80000     | -     |
    +---------------------------------------------------+-----------+-------+
    | relationship_incoming_blocked                     | 80001     | -     |
    +---------------------------------------------------+-----------+-------+
    | relationship_invalid_user_bot                     | 80002     | -     |
    +---------------------------------------------------+-----------+-------+
    | relationship_invalid_self                         | 80003     | -     |
    +---------------------------------------------------+-----------+-------+
    | relationship_invalid_discord_tag                  | 80004     | -     |
    +---------------------------------------------------+-----------+-------+
    | reaction_blocked                                  | 90001     | -     |
    +---------------------------------------------------+-----------+-------+
    | listing_already_joined                            | 120000    | -     |
    +---------------------------------------------------+-----------+-------+
    | listing_too_many_member                           | 120001    | -     |
    +---------------------------------------------------+-----------+-------+
    | listing_join_blocked                              | 120002    | -     |
    +---------------------------------------------------+-----------+-------+
    | resource_overloaded                               | 130000    | -     |
    +---------------------------------------------------+-----------+-------+
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
    unknown_webhook_service = 10016
    unknown_ban             = 10026
    unknown_SKU             = 10027
    unknown_store_listing   = 10028
    unknown_entitlement     = 10029
    unknown_build           = 10030
    unknown_lobby           = 10031
    unknown_branch          = 10032
    unknown_redistributable = 10036
    unknown_gift_code       = 10038
    unknown_guild_template  = 10057
    unknown_discovery_category = 10059
    unknown_interaction     = 10062
    unknown_application_command = 10063
    
    bots_not_allowed        = 20001
    only_bots_allowed       = 20002
    RPC_proxy_disallowed    = 20003
    explicit_content        = 20009
    account_scheduled_for_deletion = 20011
    user_not_authorized_for_application = 20012
    account_disabled        = 20013
    slowmode_rate_limited    = 20016
    channel_following_edit_rate_limited = 20022
    under_minimum_age       = 20024
    channel_send_rate_limit = 20028
    
    max_guilds              = 30001 # 100
    max_friends             = 30001 # 10000
    max_pins                = 30003 # 50
    max_recipients          = 30004
    max_roles               = 30005 # 250
    max_used_usernames      = 30006
    max_webhooks            = 30007 # 10
    max_emoji               = 30008
    max_reactions           = 30010 # 20
    max_channels            = 30013 # 500
    max_attachments         = 30015 # 10
    max_invites             = 30016 # 1000
    max_animated_emoji      = 30018
    not_enough_guild_members = 30029
    max_guild_discovery_category = 30030 # 5
    
    unauthorized            = 40001
    email_verification_required = 40002
    rate_limit_DM_open      = 40003
    send_message_temporarily_disabled = 40004
    request_too_large       = 40005
    feature_disabled        = 40006
    user_banned             = 40007
    connection_rewoked      = 40012
    delete_account_transfer_team_ownership = 40028
    user_not_connected      = 40032
    message_already_crossposted = 40033
    
    invalid_access          = 50001
    invalid_account_type    = 50002
    invalid_action_DM       = 50003
    invalid_widget_disabled = 50004
    invalid_message_author  = 50005
    invalid_message_empty   = 50006
    cannot_message_user     = 50007
    invalid_message_send_non_text = 50008
    invalid_message_verification_level = 50009
    invalid_oauth_app_bot   = 50010
    invalid_oauth_app_limit = 50011
    invalid_oauth_state     = 50012
    invalid_permissions     = 50013
    invalid_token           = 50014
    invalid_note            = 50015
    invalid_bulk_delete_count = 50016
    invalid_MFA_level       = 50017
    invalid_password        = 50018
    invalid_pin_message_channel = 50019
    invalid_or_taken_invite_code = 50020
    invalid_message_system  = 50021
    invalid_phone_number    = 50022
    invalid_client_id       = 50023
    invalid_channel_type    = 50024
    invalid_oauth2_access_token = 50025
    invalid_oauth2_missing_scope = 50026
    invalid_webhook_token   = 50027
    invalid_recipients      = 50033
    invalid_bulk_delete_message_age = 50034
    invalid_form_body       = 50035
    cannot_add_user_to_guild_where_bot_is_not = 50036
    invalid_API_version     = 50041
    invalid_gift_redemption_exhausted = 50050
    invalid_gift_redemption_owned = 50051
    invalid_gift_self_redemption = 50054
    invalid_message_type    = 50068
    cannot_delete_community_channel = 50074
    invalid_sticker_sent    = 50081
    invalid_gift_redemption_subscription_managed = 100021
    invalid_gift_redemption_subscription_incompatible = 100023
    invalid_gift_redemption_invoice_open = 100024
    
    MFA_enabled             = 60001
    MFA_disabled            = 60002
    MFA_required            = 60003
    MFA_unverified          = 60004
    MFA_invalid_secret      = 60005
    MFA_invalid_ticket      = 60006
    MFA_invalid_code        = 60008
    MFA_invalid_session     = 60009
    
    phone_number_unable_to_send = 70003
    
    relationship_incoming_disabled = 80000
    relationship_incoming_blocked = 80001
    relationship_invalid_user_bot = 80002
    relationship_invalid_self   = 80003
    relationship_invalid_discord_tag = 80004
    
    reaction_blocked        = 90001
    
    listing_already_joined  = 120000
    listing_too_many_member = 120001
    listing_join_blocked    = 120002
    
    resource_overloaded     = 130000

class DiscordGatewayException(BaseException):
    """
    An intent error is raised by a ``DiscordGateway`` when a ``Client`` tries to log in with an invalid intent value.
    
    Attributes
    ----------
    code : `int`
        Gateway close code sent by Discord.
    
    Class Attributes
    ----------------
    CODETABLE : `dict` of (`int`, `str`) items
        A dictionary to store the descriptions for each gateway close code.
    INTENT_ERROR_CODES : `tuple` (`str`, `str`) = (`4013`, `4014`)
        Close codes of intent errors.
    RESHARD_ERROR_CODES : `tuple` (`int`,) = (`4011`,)
    """
    INTENT_ERROR_CODES = (4013, 4014)
    RESHARD_ERROR_CODES = (4011,)
    
    CODETABLE = {
        4011 : 'A gateway would have handled too many guilds, resharding is required.',
        4013 : 'An invalid intent is one that is not meaningful and not documented.',
        4014 : 'A disallowed intent is one which you have not enabled for your bot or one that your bot is not '
               'whitelisted to use.',
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

class InvalidToken(BaseException):
    def __init__(self):
        BaseException.__init__(self,'Invalid token, please update it, then start the client again.')
    

VOICE_CLIENT_DISCONNECT_CLOSE_CODE = 4014
