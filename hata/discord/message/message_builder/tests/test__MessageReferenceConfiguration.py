import vampytest

from ..message_reference_configuration import MessageReferenceConfiguration
from ..preinstanced import MessageReferenceType


def _assert_fields_set(message_reference_configuration):
    """
    Asserts whether every fields are set of the message reference configuration.
    
    Parameters
    ----------
    message_reference_configuration : ``MessageReferenceConfiguration``
        The message reference configuration to test.
    """
    vampytest.assert_instance(message_reference_configuration, MessageReferenceConfiguration)
    vampytest.assert_instance(message_reference_configuration.channel_id, int)
    vampytest.assert_instance(message_reference_configuration.fail_fallback, bool)
    vampytest.assert_instance(message_reference_configuration.message_id, int)
    vampytest.assert_instance(message_reference_configuration.type, MessageReferenceType)


def test__MessageReferenceConfiguration__new__no_fields():
    """
    Tests whether ``MessageReferenceConfiguration.__new__`` works as intended.
    
    Case: No fields given.
    """
    message_reference_configuration = MessageReferenceConfiguration()
    _assert_fields_set(message_reference_configuration)


def test__MessageReferenceConfiguration__new__all_fields():
    """
    Tests whether ``MessageReferenceConfiguration.__new__`` works as intended.
    
    Case: All fields given.
    """
    channel_id = 202405220002
    message_id = 202303070000
    fail_fallback = True
    message_reference_type = MessageReferenceType.forward
    
    message_reference_configuration = MessageReferenceConfiguration(
        channel_id = channel_id,
        fail_fallback = fail_fallback,
        message_id = message_id,
        message_reference_type = message_reference_type,
    )
    _assert_fields_set(message_reference_configuration)
    
    vampytest.assert_eq(message_reference_configuration.channel_id, channel_id)
    vampytest.assert_eq(message_reference_configuration.fail_fallback, fail_fallback)
    vampytest.assert_eq(message_reference_configuration.message_id, message_id)
    vampytest.assert_is(message_reference_configuration.type, message_reference_type)


def _iter_options__to_data():
    channel_id = 202405220003
    message_id = 202303070001
    
    yield {}, {'message_id': str(0)}
    
    yield {'message_id': message_id}, {'message_id': str(message_id)}
    yield {'fail_fallback': True}, {'message_id': str(0), 'fail_if_not_exists': False}
    yield (
        {'fail_fallback': True, 'message_id': message_id},
        {'message_id': str(message_id), 'fail_if_not_exists': False},
    )
    yield (
        {'channel_id': channel_id, 'message_id': message_id, 'message_reference_type': MessageReferenceType.forward},
        {'channel_id': str(channel_id), 'message_id': str(message_id), 'type': MessageReferenceType.forward.value},
    )


@vampytest._(vampytest.call_from(_iter_options__to_data()).returning_last())
def test__MessageReferenceConfiguration__to_data(keyword_parameters):
    """
    Tests whether ``MessageReferenceConfiguration`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create reply configuration with.
    """
    message_reference_configuration = MessageReferenceConfiguration(**keyword_parameters)
    return message_reference_configuration.to_data()
    

def _iter_options__bool():
    channel_id = 202405220004
    message_id = 202303070002
    
    yield {}, False
    
    yield {'message_id': message_id}, True
    yield {'fail_fallback': True}, False
    yield (
        {'fail_fallback': True, 'message_id': message_id},
        True,
    )
    yield {'channel_id': channel_id}, False
    yield {'message_reference_type': MessageReferenceType.forward}, False


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__MessageReferenceConfiguration__bool(keyword_parameters):
    """
    Tests whether ``MessageReferenceConfiguration.__bool__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create reply configuration with.
    
    Returns
    -------
    output : `bool`
    """
    message_reference_configuration = MessageReferenceConfiguration(**keyword_parameters)
    output = bool(message_reference_configuration)
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__eq__different_type():
    yield None, False
    yield object(), False


@vampytest._(vampytest.call_from(_iter_options__eq__different_type()).returning_last())
def test__MessageReferenceConfiguration__eq__different_type(other_value):
    """
    Tests whether ``MessageReferenceConfiguration.__eq__`` works as intended.
    
    Case: different type.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create reply configuration with.
    other_value : `object`
        Other value to compare to.
    
    Returns
    -------
    output : `bool`
    """
    message_reference_configuration = MessageReferenceConfiguration()
    
    output = message_reference_configuration == other_value
    
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__eq__same_type():
    channel_id = 202405220005
    message_id = 202303070003
    
    yield {}, {}, True
    
    yield (
        {'message_id': message_id},
        {'message_id': message_id},
        True,
    )
    
    yield (
        {'message_id': message_id},
        {'message_id': 202303070004},
        False,
    )
    
    yield (
        {'fail_fallback': True},
        {'fail_fallback': True},
        True,
    )
    
    yield (
        {'fail_fallback': True},
        {'fail_fallback': False},
        False,
    )
    
    yield (
        {'channel_id': channel_id},
        {'channel_id': channel_id},
        True,
    )
    
    yield (
        {'channel_id': channel_id},
        {'channel_id': 202405220006},
        False,
    )
    
    yield (
        {'message_reference_type': MessageReferenceType.reply},
        {'message_reference_type': MessageReferenceType.reply},
        True,
    )
    
    yield (
        {'message_reference_type': MessageReferenceType.reply},
        {'message_reference_type': MessageReferenceType.forward},
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq__same_type()).returning_last())
def test__MessageReferenceConfiguration__eq__same_type(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``MessageReferenceConfiguration.__eq__`` works as intended.
    
    Case: same type.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create reply configuration with.
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create reply configuration with.
    
    Returns
    -------
    output : `bool`
    """
    message_reference_configuration_0 = MessageReferenceConfiguration(**keyword_parameters_0)
    message_reference_configuration_1 = MessageReferenceConfiguration(**keyword_parameters_1)
    
    output = message_reference_configuration_0 == message_reference_configuration_1
    
    vampytest.assert_instance(output, bool)
    return output


def test__MessageReferenceConfiguration__repr():
    """
    Tests whether ``MessageReferenceConfiguration.__repr__`` works as intended.
    """
    channel_id = 202405220007
    message_id = 202303070005
    fail_fallback = True
    message_reference_type = MessageReferenceType.forward
    
    message_reference_configuration = MessageReferenceConfiguration(
        channel_id = channel_id,
        fail_fallback = fail_fallback,
        message_id = message_id,
        message_reference_type = message_reference_type,
    )
    
    output = repr(message_reference_configuration)
    
    vampytest.assert_instance(output, str)


def _iter_options__or():
    channel_id_0 = 202405220008
    channel_id_1 = 202405220009
    message_id_0 = 202303070006
    message_id_1 = 202303070007
    
    yield (
        {},
        {},
        {},
    )
    
    yield (
        {'channel_id': channel_id_0},
        {'channel_id': channel_id_0},
        {'channel_id': channel_id_0},
    )
    
    yield (
        {'channel_id': channel_id_0},
        {'channel_id': 0},
        {'channel_id': channel_id_0},
    )
    
    yield (
        {'channel_id': channel_id_0},
        {'channel_id': channel_id_1},
        {'channel_id': channel_id_1},
    )
    
    yield (
        {'message_id': message_id_0},
        {'message_id': message_id_0},
        {'message_id': message_id_0},
    )
    
    yield (
        {'message_id': message_id_0},
        {'message_id': 0},
        {'message_id': message_id_0},
    )
    
    yield (
        {'message_id': message_id_0},
        {'message_id': message_id_1},
        {'message_id': message_id_1},
    )
    
    yield (
        {'fail_fallback': True},
        {'fail_fallback': True},
        {'fail_fallback': True},
    )
    
    yield (
        {'fail_fallback': True},
        {'fail_fallback': False},
        {'fail_fallback': True},
    )
    
    yield (
        {'fail_fallback': False},
        {'fail_fallback': True},
        {'fail_fallback': True},
    )

    
    yield (
        {'message_reference_type': MessageReferenceType.forward},
        {'message_reference_type': MessageReferenceType.forward},
        {'message_reference_type': MessageReferenceType.forward},
    )
    
    yield (
        {'message_reference_type': MessageReferenceType.forward},
        {'message_reference_type': MessageReferenceType.reply},
        {'message_reference_type': MessageReferenceType.forward},
    )
    
    yield (
        {'message_reference_type': MessageReferenceType.reply},
        {'message_reference_type': MessageReferenceType.forward},
        {'message_reference_type': MessageReferenceType.forward},
    )


@vampytest._(vampytest.call_from(_iter_options__or()))
def test__MessageReferenceConfiguration__or(keyword_parameters_0, keyword_parameters_1, keyword_parameters_2):
    """
    Tests whether ``MessageReferenceConfiguration.__or__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create reply configuration with.
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create reply configuration with.
    keyword_parameters_2 : `dict<str, object>`
        Keyword parameters to create reply configuration with.
    
    Returns
    -------
    output : `bool`
    """
    message_reference_configuration_0 = MessageReferenceConfiguration(**keyword_parameters_0)
    message_reference_configuration_1 = MessageReferenceConfiguration(**keyword_parameters_1)
    message_reference_configuration_2 = MessageReferenceConfiguration(**keyword_parameters_2)
    
    output = message_reference_configuration_0 | message_reference_configuration_1
    
    _assert_fields_set(output)
    vampytest.assert_eq(output, message_reference_configuration_2)
