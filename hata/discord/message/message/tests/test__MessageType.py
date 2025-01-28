from datetime import datetime as DateTime, timezone as TimeZone
from types import FunctionType

import vampytest

from ....embed import Embed, EmbedType
from ....emoji import Emoji
from ....user import User

from ..message import Message
from ..preinstanced import MESSAGE_DEFAULT_CONVERTER, MessageType

from ...message_call import MessageCall


def _assert_fields_set(message_type):
    """
    Asserts whether every field are set of the given message type.
    
    Parameters
    ----------
    message_type : ``MessageType``
        The instance to test.
    """
    vampytest.assert_instance(message_type, MessageType)
    vampytest.assert_instance(message_type.name, str)
    vampytest.assert_instance(message_type.value, MessageType.VALUE_TYPE)
    vampytest.assert_instance(message_type.converter, FunctionType)
    vampytest.assert_instance(message_type.deletable, bool)


@vampytest.call_from(MessageType.INSTANCES.values())
def test__MessageType__instances(instance):
    """
    Tests whether ``MessageType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``MessageType``
        The instance to test.
    """
    _assert_fields_set(instance)


def test__MessageType__new__min_fields():
    """
    Tests whether ``MessageType.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    value = 50
    
    try:
        output = MessageType(value)
        _assert_fields_set(output)
        
        vampytest.assert_eq(output.value, value)
        vampytest.assert_eq(output.name, MessageType.NAME_DEFAULT)
        vampytest.assert_is(output.converter, MESSAGE_DEFAULT_CONVERTER)
        vampytest.assert_eq(output.deletable, True)
        vampytest.assert_is(MessageType.INSTANCES.get(value, None), output)
    
    finally:
        try:
            del MessageType.INSTANCES[value]
        except KeyError:
            pass



def _iter_options__call():
    ended_at = DateTime(2016, 4, 4, tzinfo = TimeZone.utc)
    user_0 = User.precreate(202305060000)
    user_1 = User.precreate(202305060001)
    
    yield Message()
    yield Message(author = user_0),
    yield Message(author = user_0, call = MessageCall())
    yield Message(author = user_0, call = MessageCall(ended_at = ended_at))
    yield Message(author = user_0, call = MessageCall(user_ids = [user_0.id]))
    yield Message(author = user_0, call = MessageCall(user_ids = [user_0.id, user_1.id]))
    yield Message(author = user_0, call = MessageCall(ended_at = ended_at, user_ids = [user_0.id, user_1.id]))


@vampytest.call_from(_iter_options__call())
def test__MessageType__call(message):
    """
    Tests whether ``MessageType.call`` conversion not fails.
    
    Parameters
    ----------
    message : ``Message``
        Message to test with.
    """
    output = MessageType.call.converter(message)
    vampytest.assert_instance(output, str, nullable = True)


def _iter_options__poll_result():
    emoji = Emoji.precreate(772496201642934272, name = 'KoishiYay')
    
    yield Message(), None
    
    yield (
        Message(
            embeds = [
                Embed(
                    embed_type = EmbedType.poll_result,
                ).add_field(
                    'poll_question_text',
                    'Hey mister',
                ).add_field(
                    'victor_answer_text',
                    'Remilia',
                ).add_field(
                    'victor_answer_votes',
                    '1',
                ).add_field(
                    'total_votes',
                    '2',
                ).add_field(
                    'victor_answer_emoji_id',
                    str(emoji.id),
                ).add_field(
                    'victor_answer_emoji_name',
                    emoji.name,
                )
            ],
        ),
        (
            f'The poll Hey mister has closed.\n'
            f'{emoji} Remilia\n'
            f'Winning answer • 50%'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__poll_result()).returning_last())
def test__MessageType__poll_result(message):
    """
    Tests whether ``MessageType.poll_result`` conversion not fails.
    
    Parameters
    ----------
    message : ``Message``
        Message to test with.
    
    Returns
    -------
    output : `None | str`
    """
    output = MessageType.poll_result.converter(message)
    vampytest.assert_instance(output, str, nullable = True)
    return output
