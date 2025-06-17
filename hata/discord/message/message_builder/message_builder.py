__all__ = (
    'MessageBuilderForumThreadCreate', 'MessageBuilderBase', 'MessageBuilderCreate', 'MessageBuilderEdit',
    'MessageBuilderInteractionComponentEdit', 'MessageBuilderInteractionFollowupCreate',
    'MessageBuilderInteractionFollowupEdit', 'MessageBuilderInteractionResponseCreate',
    'MessageBuilderInteractionResponseEdit', 'MessageBuilderWebhookCreate', 'MessageBuilderWebhookEdit'
)

from scarletio import copy_docs, export

from ...builder.builder_fielded import BuilderFielded

from .conversions import (
    CONVERSION_ALLOWED_MENTIONS, CONVERSION_APPLIED_TAGS, CONVERSION_APPLIED_TAG_IDS, CONVERSION_ATTACHMENTS,
    CONVERSION_AVATAR_URL, CONVERSION_COMPONENTS, CONVERSION_CONTENT, CONVERSION_EMBED, CONVERSION_EMBEDS,
    CONVERSION_ENFORCE_NONCE, CONVERSION_FLAGS, CONVERSION_FORWARD_MESSAGE, CONVERSION_INSTANCE,
    CONVERSION_MESSAGE_REFERENCE_CONFIGURATION, CONVERSION_NAME, CONVERSION_NONCE, CONVERSION_POLL,
    CONVERSION_REPLY_FAIL_FALLBACK, CONVERSION_REPLY_MESSAGE_ID, CONVERSION_SHOW_FOR_INVOKING_USER_ONLY,
    CONVERSION_SILENT, CONVERSION_STICKER, CONVERSION_STICKERS, CONVERSION_STICKER_IDS, CONVERSION_SUPPRESS_EMBEDS,
    CONVERSION_THREAD_NAME, CONVERSION_TTS, CONVERSION_VOICE_ATTACHMENT
)


@export
class MessageBuilderBase(BuilderFielded):
    """
    Base message builder.
    
    Attributes
    ----------
    fields : `dict<Conversion, object>`
        The fields to create the message with.
    """
    __slots__ = ()
    
    __conversions_default__ = [
        CONVERSION_INSTANCE,
    ]
    
    
    @copy_docs(BuilderFielded._with_positional_parameter_unknown)
    def _with_positional_parameter_unknown(self, value):
        return self._setter_field(CONVERSION_CONTENT, str(value))
    
    
    allowed_mentions = CONVERSION_ALLOWED_MENTIONS
    components = CONVERSION_COMPONENTS
    content = CONVERSION_CONTENT
    embed = CONVERSION_EMBED
    embeds = CONVERSION_EMBEDS
    flags = CONVERSION_FLAGS
    suppress_embeds = CONVERSION_SUPPRESS_EMBEDS


class MessageBuilderCreate(MessageBuilderBase):
    """
    Message builder for ``Client.message_create`` method.
    
    Attributes
    ----------
    fields : `dict<Conversion, object>`
        The fields to create the message with.
    """
    __slots__ = ()
    
    attachments = CONVERSION_ATTACHMENTS
    enforce_nonce = CONVERSION_ENFORCE_NONCE
    forward_message = CONVERSION_FORWARD_MESSAGE
    message_reference_configuration = CONVERSION_MESSAGE_REFERENCE_CONFIGURATION
    nonce = CONVERSION_NONCE
    poll = CONVERSION_POLL
    reply_fail_fallback = CONVERSION_REPLY_FAIL_FALLBACK
    reply_message_id = CONVERSION_REPLY_MESSAGE_ID
    silent = CONVERSION_SILENT
    sticker = CONVERSION_STICKER
    sticker_ids = CONVERSION_STICKER_IDS
    stickers = CONVERSION_STICKERS
    tts = CONVERSION_TTS
    voice_attachment = CONVERSION_VOICE_ATTACHMENT


class MessageBuilderEdit(MessageBuilderBase):
    """
    Message builder for ``Client.message_edit`` method.
    
    Attributes
    ----------
    fields : `dict<Conversion, object>`
        The fields to create the message with.
    """
    __slots__ = ()
    
    attachments = CONVERSION_ATTACHMENTS


class MessageBuilderWebhookCreate(MessageBuilderBase):
    """
    Message builder for ``Client.webhook_message_create``.
    
    Attributes
    ----------
    fields : `dict<Conversion, object>`
        The fields to create the message with.
    """
    __slots__ = ()
    
    applied_tags = CONVERSION_APPLIED_TAGS
    applied_tag_ids = CONVERSION_APPLIED_TAG_IDS
    attachments = CONVERSION_ATTACHMENTS
    avatar_url = CONVERSION_AVATAR_URL
    name = CONVERSION_NAME
    poll = CONVERSION_POLL
    silent = CONVERSION_SILENT
    thread_name = CONVERSION_THREAD_NAME
    tts = CONVERSION_TTS
    voice_attachment = CONVERSION_VOICE_ATTACHMENT


class MessageBuilderWebhookEdit(MessageBuilderEdit):
    """
    Message builder for ``Client.webhook_message_edit``.
    
    Attributes
    ----------
    fields : `dict<Conversion, object>`
        The fields to create the message with.
    """
    __slots__ = ()
    
    
class MessageBuilderForumThreadCreate(MessageBuilderBase):
    """
    Message builder for ``Client.forum_thread_create`` method.
    
    Attributes
    ----------
    fields : `dict<Conversion, object>`
        The fields to create the message with.
    """
    __slots__ = ()
    
    attachments = CONVERSION_ATTACHMENTS
    nonce = CONVERSION_NONCE
    silent = CONVERSION_SILENT
    sticker = CONVERSION_STICKER
    sticker_ids = CONVERSION_STICKER_IDS
    stickers = CONVERSION_STICKERS
    tts = CONVERSION_TTS


class MessageBuilderInteractionComponentEdit(MessageBuilderBase):
    """
    Message builder for ``Client.interaction_component_message_edit``.
    
    Attributes
    ----------
    fields : `dict<Conversion, object>`
        The fields to create the message with.
    """
    __slots__ = ()


class MessageBuilderInteractionFollowupCreate(MessageBuilderBase):
    """
    Message builder for ``Client.interaction_followup_message_create` method.
    
    Attributes
    ----------
    fields : `dict<Conversion, object>`
        The fields to create the message with.
    """
    __slots__ = ()
    
    attachments = CONVERSION_ATTACHMENTS
    poll = CONVERSION_POLL
    show_for_invoking_user_only = CONVERSION_SHOW_FOR_INVOKING_USER_ONLY
    silent = CONVERSION_SILENT
    tts = CONVERSION_TTS
    voice_attachment = CONVERSION_VOICE_ATTACHMENT


class MessageBuilderInteractionFollowupEdit(MessageBuilderEdit):
    """
    Message builder for ``Client.interaction_followup_message_edit``.
    
    Attributes
    ----------
    fields : `dict<Conversion, object>`
        The fields to create the message with.
    """
    __slots__ = ()


class MessageBuilderInteractionResponseCreate(MessageBuilderBase):
    """
    Message builder for ``Client.interaction_response_message_create` method.
    
    Attributes
    ----------
    fields : `dict<Conversion, object>`
        The fields to create the message with.
    """
    __slots__ = ()
    
    poll = CONVERSION_POLL
    show_for_invoking_user_only = CONVERSION_SHOW_FOR_INVOKING_USER_ONLY
    silent = CONVERSION_SILENT
    tts = CONVERSION_TTS


class MessageBuilderInteractionResponseEdit(MessageBuilderEdit):
    """
    Message builder for ``Client.interaction_response_message_edit``.
    
    Attributes
    ----------
    fields : `dict<Conversion, object>`
        The fields to create the message with.
    """
    __slots__ = ()
    
    poll = CONVERSION_POLL
    voice_attachment = CONVERSION_VOICE_ATTACHMENT
