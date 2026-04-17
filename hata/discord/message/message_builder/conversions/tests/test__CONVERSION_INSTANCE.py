import vampytest

from ..instance import CONVERSION_INSTANCE

from ...message_builder import MessageBuilderBase


def _iter_options__set_identifier():
    yield object(), []
    yield None, []
    
    message_builder = MessageBuilderBase()
    message_builder.content = 'mister'
    yield message_builder, [message_builder]


@vampytest._(vampytest.call_from(_iter_options__set_identifier()).returning_last())
def test__CONVERSION_INSTANCE__set_identifier(input_value):
    """
    Tests whether ``CONVERSION_INSTANCE.set_identifier`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<MessageBuilderBase>`
    """
    return [*CONVERSION_INSTANCE.set_identifier(input_value)]

