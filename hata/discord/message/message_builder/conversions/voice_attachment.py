__all__ = ('CONVERSION_VOICE_ATTACHMENT',)

from scarletio.web_common import FormData

from .....env import API_VERSION

from ....builder.constants import CONVERSION_KIND_FIELD
from ....builder.conversion import Conversion

from ...message import MessageFlag
from ...voice_attachment import VoiceAttachment


MESSAGE_FLAG_VOICE_MESSAGE = MessageFlag().update_by_keys(voice_message = True)


def _preprocess_data_and_check_empty(data, voice_attachment):
    """
    Preprocesses the data and checks whether it is empty.
    
    Parameters
    ----------
    data : ``dict<str, object> | FormData>``
        The data to preprocess.
    
    Returns
    -------
    form : ``FormData``
    
    Raises
    ------
    ValueError
        - if the given `data` is not empty.
    """
    while True:
        if isinstance(data, dict):
            if (
                ('content' in data) or
                ('embed' in data) or
                ('attachments' in data) or
                ('components' in data) or
                ('poll' in data)
            ):
                break
            
            data['attachments'] = [voice_attachment.to_data()]
            data['flags'] = data.get('flags', 0) | MESSAGE_FLAG_VOICE_MESSAGE
            
            form = FormData()
            form.add_json('payload_json', data)
        
        elif isinstance(data, FormData):
            break
        
        else:
            # Unexpected case
            break
        
        return form
    
    raise ValueError(
        f'When sending voice messages, `voice_attachment` should be the only set field.'
    )


class CONVERSION_VOICE_ATTACHMENT(Conversion):
    # Generic
    
    name = 'voice_attachment'
    name_aliases = None
    expected_types_messages = VoiceAttachment.__name__
    kind = CONVERSION_KIND_FIELD
    output_conversion = None
    
    # Setting
    
    set_merger = None
    set_type = VoiceAttachment
    set_type_processor = None
    set_identifier = None
    set_listing_identifier = None
    
    def set_validator(value):
        """
        Yields the outcome if `value` is acceptable.
        
        Parameters
        ----------
        value : ``VoiceAttachment``
            The value to check.
        
        Yields
        ------
        voice_attachment : ``None | VoiceAttachment``
        """
        # None
        if value is None:
            yield None
            return
        
        # VoiceAttachment
        if isinstance(value, VoiceAttachment):
            yield value
            return
    
    
    # Reading
    
    get_default = None
    get_processor = None
    
    
    # Serialization
    
    serializer_key = None
    serializer_optional = None
    serializer_required = None
    
    
    if API_VERSION >= 9:
        def serializer_putter(data, required, value):
            if value is None:
                return data
            
            form = _preprocess_data_and_check_empty(data, value)
            form.add_field('files[0]', value.io, file_name = value.name, content_type = 'application/octet-stream')
            return form
    
    else:
        # On lower versions voice attachments are not supported, attach them as regular attachments instead.
        def serializer_putter(data, required, value):
            if value is None:
                return data
            
            form = _preprocess_data_and_check_empty(data, value)
            form.add_field('file', value.io, file_name = value.name, content_type = 'application/octet-stream')
            return form
    
    
    # Sorting
    
    sort_priority = 10000
