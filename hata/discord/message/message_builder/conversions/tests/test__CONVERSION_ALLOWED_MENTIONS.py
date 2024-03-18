import vampytest

from .....allowed_mentions import AllowedMentionProxy
from .....role import Role
from .....user import User

from ..allowed_mentions import CONVERSION_ALLOWED_MENTIONS


def _iter_options__set_merger():
    yield ['users'], ['roles'], AllowedMentionProxy('users', 'roles')
    yield AllowedMentionProxy('users'), AllowedMentionProxy('roles'), AllowedMentionProxy('users', 'roles')


@vampytest._(vampytest.call_from(_iter_options__set_merger()).returning_last())
def test__CONVERSION_ALLOWED_MENTIONS__set_merger(input_value_0, input_value_1):
    """
    Tests whether ``CONVERSION_ALLOWED_MENTIONS.set_merger`` works as intended.
    
    Parameters
    ----------
    input_value_0 : `object`
        Value to test.
    input_value_1 : `object`
        Value to test.
    
    Returns
    -------
    output : ``AllowedMentionProxy``
    """
    output = CONVERSION_ALLOWED_MENTIONS.set_merger(input_value_0, input_value_1)
    vampytest.assert_instance(output, AllowedMentionProxy)
    return output


def _iter_options__set_validator():
    yield object(), []
    yield None, [None]
    yield 'mister', []
    yield ['mister'], []
    yield 'users', []
    yield ['users'], [['users']]
    yield Role.precreate(202302220004), []
    yield [Role.precreate(202302220005)], [[Role.precreate(202302220005)]]
    yield User.precreate(202302220006), []
    yield [User.precreate(202302220007)], [[User.precreate(202302220007)]]
    yield AllowedMentionProxy('roles'), [AllowedMentionProxy('roles')]


@vampytest._(vampytest.call_from(_iter_options__set_validator()).returning_last())
def test__CONVERSION_ALLOWED_MENTIONS__set_validator(input_value):
    """
    Tests whether ``CONVERSION_ALLOWED_MENTIONS.set_validator`` works as intended.
    
    Parameters
    ----------
    input_value : `object`
        Value to test.
    
    Returns
    -------
    output : `list<None | str>`
    """
    return [*CONVERSION_ALLOWED_MENTIONS.set_validator(input_value)]


def _iter_options__serializer_optional():
    yield None, [{'parse': []}]
    yield ['users', 'roles'], [{'parse': ['users', 'roles']}]
    yield AllowedMentionProxy('everyone'), [{'parse': ['everyone']}]


@vampytest._(vampytest.call_from(_iter_options__serializer_optional()).returning_last())
def test__CONVERSION_ALLOWED_MENTIONS__serializer_optional(input_value):
    """
    Tests whether ``CONVERSION_ALLOWED_MENTIONS.serializer_optional`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<object> | AllowedMentionProxy`
        Value to test.
    
    Returns
    -------
    output : `list<dict<str, object>>`
    """
    return [*CONVERSION_ALLOWED_MENTIONS.serializer_optional(input_value)]


def _iter_options__serializer_required():
    yield None, {'parse': []}
    yield ['users', 'roles'], {'parse': ['users', 'roles']}
    yield AllowedMentionProxy('everyone'), {'parse': ['everyone']}


@vampytest._(vampytest.call_from(_iter_options__serializer_required()).returning_last())
def test__CONVERSION_ALLOWED_MENTIONS__serializer_required(input_value):
    """
    Tests whether ``CONVERSION_ALLOWED_MENTIONS.serializer_required`` works as intended.
    
    Parameters
    ----------
    input_value : `None | list<object> | AllowedMentionProxy`
        Value to test.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return CONVERSION_ALLOWED_MENTIONS.serializer_required(input_value)
