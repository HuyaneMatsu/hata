import vampytest

from .....discord.application_command import ApplicationCommandTargetType

from ..helpers import validate_application_target_type


def _iter_options__passing():
    yield None, ApplicationCommandTargetType.chat
    yield ApplicationCommandTargetType.none, ApplicationCommandTargetType.chat
    
    yield ApplicationCommandTargetType.chat, ApplicationCommandTargetType.chat
    yield ApplicationCommandTargetType.chat.name, ApplicationCommandTargetType.chat
    yield ApplicationCommandTargetType.chat.value, ApplicationCommandTargetType.chat
    
    yield ApplicationCommandTargetType.message, ApplicationCommandTargetType.message
    yield ApplicationCommandTargetType.message.name, ApplicationCommandTargetType.message
    yield ApplicationCommandTargetType.message.value, ApplicationCommandTargetType.message


def _iter_options__type_error():
    yield 12.6
    yield object()


def _iter_options__value_error():
    yield ''
    yield 'nyan'
    yield -1


@vampytest._(vampytest.call_from(_iter_options__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__value_error()).raising(ValueError))
def test__validate_application_target_type(input_value):
    """
    Tests whether ``validate_application_target_type`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Input value.
    
    Returns
    -------
    output : ``ApplicationCommandTargetType``
    
    Raises
    ------
    TypeError
    """
    output = validate_application_target_type(input_value)
    vampytest.assert_instance(output, ApplicationCommandTargetType)
    return output
