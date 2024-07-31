from datetime import datetime as DateTime, timezone as TimeZone
from types import FunctionType

import vampytest

from ....embed import Embed, EmbedType
from ....user import User

from ..message import Message
from ..preinstanced import MessageType

from ...message_call import MessageCall


@vampytest.call_from(MessageType.INSTANCES.values())
def test__MessageType__instances(instance):
    """
    Tests whether ``MessageType`` instances have the correct structure.
    
    Parameters
    ----------
    instance : ``MessageType``
        The instance to test.
    """
    vampytest.assert_instance(instance, MessageType)
    vampytest.assert_instance(instance.name, str)
    vampytest.assert_instance(instance.value, MessageType.VALUE_TYPE)
    vampytest.assert_instance(instance.converter, FunctionType)
    vampytest.assert_instance(instance.deletable, bool)



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
                ),
            ],
        ),
        (
            'The poll Hey mister has closed.\n'
            'Remilia\n'
            'Winning answer • 50%'
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
