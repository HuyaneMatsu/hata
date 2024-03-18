import vampytest

from ..reply_configuration import ReplyConfiguration


def _assert_fields_set(reply_configuration):
    """
    Asserts whether every fields are set of teh reply configuration.
    
    Parameters
    ----------
    reply_configuration : ``ReplyConfiguration``
        The reply configuration to test.
    """
    vampytest.assert_instance(reply_configuration, ReplyConfiguration)
    vampytest.assert_instance(reply_configuration.message_id, int)
    vampytest.assert_instance(reply_configuration.fail_fallback, bool)


def test__ReplyConfiguration__new__no_fields():
    """
    Tests whether ``ReplyConfiguration.__new__`` works as intended.
    
    Case: No fields given.
    """
    reply_configuration = ReplyConfiguration()
    _assert_fields_set(reply_configuration)


def test__ReplyConfiguration__new__all_fields():
    """
    Tests whether ``ReplyConfiguration.__new__`` works as intended.
    
    Case: All fields given.
    """
    message_id = 202303070000
    fail_fallback = True
    
    reply_configuration = ReplyConfiguration(message_id = message_id, fail_fallback = fail_fallback)
    _assert_fields_set(reply_configuration)


def _iter_options__to_data():
    message_id = 202303070001
    
    yield {}, {'message_id': str(0)}
    
    yield {'message_id': message_id}, {'message_id': str(message_id)}
    yield {'fail_fallback': True}, {'message_id': str(0), 'fail_if_not_exists': False}
    yield (
        {'fail_fallback': True, 'message_id': message_id},
        {'message_id': str(message_id), 'fail_if_not_exists': False},
    )


@vampytest._(vampytest.call_from(_iter_options__to_data()).returning_last())
def test__ReplyConfiguration__to_data(keyword_parameters):
    """
    Tests whether ``ReplyConfiguration`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create reply configuration with.
    """
    reply_configuration = ReplyConfiguration(**keyword_parameters)
    return reply_configuration.to_data()
    

def _iter_options__bool():
    message_id = 202303070002
    
    yield {}, False
    
    yield {'message_id': message_id}, True
    yield {'fail_fallback': True}, False
    yield (
        {'fail_fallback': True, 'message_id': message_id},
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__bool()).returning_last())
def test__ReplyConfiguration__bool(keyword_parameters):
    """
    Tests whether ``ReplyConfiguration.__bool__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create reply configuration with.
    
    Returns
    -------
    output : `bool`
    """
    reply_configuration = ReplyConfiguration(**keyword_parameters)
    output = bool(reply_configuration)
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__eq__different_type():
    yield None, False
    yield object(), False


@vampytest._(vampytest.call_from(_iter_options__eq__different_type()).returning_last())
def test__ReplyConfiguration__eq__different_type(other_value):
    """
    Tests whether ``ReplyConfiguration.__eq__`` works as intended.
    
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
    reply_configuration = ReplyConfiguration()
    
    output = reply_configuration == other_value
    
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__eq__same_type():
    message_id_0 = 202303070003
    message_id_1 = 202303070004
    
    yield {}, {}, True
    
    yield (
        {'message_id': message_id_0},
        {'message_id': message_id_0},
        True,
    )
    
    yield (
        {'message_id': message_id_0},
        {'message_id': message_id_1},
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


@vampytest._(vampytest.call_from(_iter_options__eq__same_type()).returning_last())
def test__ReplyConfiguration__eq__same_type(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ReplyConfiguration.__eq__`` works as intended.
    
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
    reply_configuration_0 = ReplyConfiguration(**keyword_parameters_0)
    reply_configuration_1 = ReplyConfiguration(**keyword_parameters_1)
    
    output = reply_configuration_0 == reply_configuration_1
    
    vampytest.assert_instance(output, bool)
    return output


def test__ReplyConfiguration__repr():
    """
    Tests whether ``ReplyConfiguration.__repr__`` works as intended.
    """
    message_id = 202303070005
    fail_fallback = True
    
    reply_configuration = ReplyConfiguration(message_id = message_id, fail_fallback = fail_fallback)
    
    output = repr(reply_configuration)
    
    vampytest.assert_instance(output, str)


def _iter_options__or():
    message_id_0 = 202303070006
    message_id_1 = 202303070007
    
    yield {}, {}, {}
    
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


@vampytest._(vampytest.call_from(_iter_options__or()))
def test__ReplyConfiguration__or(keyword_parameters_0, keyword_parameters_1, keyword_parameters_2):
    """
    Tests whether ``ReplyConfiguration.__or__`` works as intended.
    
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
    reply_configuration_0 = ReplyConfiguration(**keyword_parameters_0)
    reply_configuration_1 = ReplyConfiguration(**keyword_parameters_1)
    reply_configuration_2 = ReplyConfiguration(**keyword_parameters_2)
    
    output = reply_configuration_0 | reply_configuration_1
    
    _assert_fields_set(output)
    vampytest.assert_eq(output, reply_configuration_2)
