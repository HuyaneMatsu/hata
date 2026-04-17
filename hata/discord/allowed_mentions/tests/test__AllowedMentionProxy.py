import vampytest

from ...channel import Channel
from ...guild import Guild
from ...role import Role
from ...user import User, UserBase

from ..constants import STATE_ALLOW_REPLIED_USER_FALSE, STATE_ALLOW_REPLIED_USER_NONE, STATE_ALLOW_REPLIED_USER_TRUE
from ..proxy import AllowedMentionProxy


def _assert_fields_set(proxy):
    """
    Asserts whether every fields of the allowed mentions proxy are set.
    
    Parameters
    ----------
    proxy : ``AllowedMentionProxy``
        The allowed mentions proxy to test.
    """
    vampytest.assert_instance(proxy, AllowedMentionProxy)
    vampytest.assert_instance(proxy._allow_everyone, int)
    vampytest.assert_instance(proxy._allow_replied_user, int)
    vampytest.assert_instance(proxy._allow_roles, int)
    vampytest.assert_instance(proxy._allow_users, int)
    vampytest.assert_instance(proxy._allowed_role_ids, list, nullable = True)
    vampytest.assert_instance(proxy._allowed_user_ids, list, nullable = True)


def _iter_options__new__passing():
    yield (
        [],
        (0, STATE_ALLOW_REPLIED_USER_NONE, 0, 0, None, None),
    )
    
    yield (
        ['users'],
        (0, STATE_ALLOW_REPLIED_USER_NONE, 0, 1, None, None),
    )
    
    yield (
        ['roles'],
        (0, STATE_ALLOW_REPLIED_USER_NONE, 1, 0, None, None),
    )
    
    yield (
        ['everyone'],
        (1, STATE_ALLOW_REPLIED_USER_NONE, 0, 0, None, None),
    )
    
    yield (
        ['users', 'roles', 'everyone'],
        (1, STATE_ALLOW_REPLIED_USER_NONE, 1, 1, None, None),
    )
    
    yield (
        [User.precreate(202402160000)],
        (0, STATE_ALLOW_REPLIED_USER_NONE, 0, 0, None, [202402160000]),
    )
    
    yield (
        [User.precreate(202402160001), User.precreate(202402160002)],
        (0, STATE_ALLOW_REPLIED_USER_NONE, 0, 0, None, [202402160001, 202402160002]),
    )
    
    yield (
        [Role.precreate(202402160003)],
        (0, STATE_ALLOW_REPLIED_USER_NONE, 0, 0, [202402160003], None),
    )
    
    yield (
        [Role.precreate(202402160004), Role.precreate(202402160005)],
        (0, STATE_ALLOW_REPLIED_USER_NONE, 0, 0, [202402160004, 202402160005], None),
    )
    
    yield (
        [User.precreate(202402160007), 'users'],
        (0, STATE_ALLOW_REPLIED_USER_NONE, 0, 1, None, None),
    )
    
    yield (
        [Role.precreate(202402160008), 'roles'],
        (0, STATE_ALLOW_REPLIED_USER_NONE, 1, 0, None, None),
    )
    
    yield (
        [User.precreate(202402160009), Role.precreate(202402160010)],
        (0, STATE_ALLOW_REPLIED_USER_NONE, 0, 0, [202402160010], [202402160009]),
    )
    
    yield (
        ['replied_user'],
        (0, STATE_ALLOW_REPLIED_USER_TRUE, 0, 0, None, None),
    )
    
    yield (
        ['!replied_user'],
        (0, STATE_ALLOW_REPLIED_USER_FALSE, 0, 0, None, None),
    )


def _iter_options__new__type_error():
    yield [Channel.precreate(202402160006)]
    yield [Guild.precreate(202402160006)]
    yield [object()]
    yield [AllowedMentionProxy('users')]


def _iter_options__new__value_error():
    yield ['mister']


@vampytest._(vampytest.call_from(_iter_options__new__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__new__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__new__value_error()).raising(ValueError))
def test__AllowedMentionProxy__new(parameters):
    """
    Tests whether ``AllowedMentionProxy.__new__`` works as intended.
    
    Parameters
    ----------
    parameters : `list<object>`
        Parameters to create the instance with.
    
    Returns
    -------
    attributes : `tuple<object>`
    
    Raises
    ------
    TypeError
    ValueError
    """
    proxy = AllowedMentionProxy(*parameters)
    _assert_fields_set(proxy)
    return (
        proxy._allow_everyone,
        proxy._allow_replied_user,
        proxy._allow_roles,
        proxy._allow_users,
        proxy._allowed_role_ids,
        proxy._allowed_user_ids,
    )


def test__AllowedMentionProxy__create_from_various__instance():
    """
    Tests whether ``AllowedMentionProxy._create_from_various`` works as intended.
    
    Case: instance.
    """
    proxy = AllowedMentionProxy('users')
    
    output = AllowedMentionProxy._create_from_various(proxy)
    _assert_fields_set(output)
    
    vampytest.assert_eq(proxy, output)


def test__AllowedMentionProxy__create_from_various__single():
    """
    Tests whether ``AllowedMentionProxy._create_from_various`` works as intended.
    
    Case: single.
    """
    output = AllowedMentionProxy._create_from_various('users')
    _assert_fields_set(output)
    vampytest.assert_eq(output, AllowedMentionProxy('users'))


def test__AllowedMentionProxy__create_from_various__list():
    """
    Tests whether ``AllowedMentionProxy._create_from_various`` works as intended.
    
    Case: list (same applies to set and tuple).
    """
    output = AllowedMentionProxy._create_from_various(['users'])
    _assert_fields_set(output)
    vampytest.assert_eq(output, AllowedMentionProxy('users'))


def _iter_options__from_data():
    yield (
        {'parse': []},
        (0, STATE_ALLOW_REPLIED_USER_NONE, 0, 0, None, None),
    )
    
    yield (
        {'parse': ['users']},
        (0, STATE_ALLOW_REPLIED_USER_NONE, 0, 1, None, None),
    )
    yield (
        {'parse': ['roles']},
        (0, STATE_ALLOW_REPLIED_USER_NONE, 1, 0, None, None),
    )
    
    yield (
        {'parse': ['everyone']},
        (1, STATE_ALLOW_REPLIED_USER_NONE, 0, 0, None, None),
    )
    
    yield (
        {'parse': ['everyone', 'users', 'roles']},
        (1, STATE_ALLOW_REPLIED_USER_NONE, 1, 1, None, None),
    )
    
    yield (
        {'users': [str(202402160020)]},
        (0, STATE_ALLOW_REPLIED_USER_NONE, 0, 0, None, [202402160020]),
    )
    
    yield (
        {'users': [str(202402160021), str(202402160022)]},
        (0, STATE_ALLOW_REPLIED_USER_NONE, 0, 0, None, [202402160021, 202402160022]),
    )
    
    yield (
        {'roles': [str(202402160023)]},
        (0, STATE_ALLOW_REPLIED_USER_NONE, 0, 0, [202402160023], None),
    )
    
    yield (
        {'roles': [str(202402160024), str(202402160025)]},
        (0, STATE_ALLOW_REPLIED_USER_NONE, 0, 0, [202402160024, 202402160025], None),
    )
    
    yield (
        {'users': [str(202402160030)], 'roles': [str(202402160029)]},
        (0, STATE_ALLOW_REPLIED_USER_NONE, 0, 0, [202402160029], [202402160030]),
    )
    
    yield (
        {'replied_user': True},
        (0, STATE_ALLOW_REPLIED_USER_TRUE, 0, 0, None, None),
    )
    
    yield (
        {'replied_user': False},
        (0, STATE_ALLOW_REPLIED_USER_FALSE, 0, 0, None, None),
    )


@vampytest._(vampytest.call_from(_iter_options__from_data()).returning_last())
def test__AllowedMentionProxy__from_data(data):
    """
    Tests whether ``AllowedMentionProxy.from_data`` works as intended.
    
    Parameters
    ----------
    data : `None | dict<str, object>`items
        Allowed mention data.
    
    Returns
    -------
    attributes : `tuple<object>`
    """
    proxy = AllowedMentionProxy.from_data(data)
    _assert_fields_set(proxy)
    return (
        proxy._allow_everyone,
        proxy._allow_replied_user,
        proxy._allow_roles,
        proxy._allow_users,
        proxy._allowed_role_ids,
        proxy._allowed_user_ids,
    )


def _iter_options__to_data():
    yield (
        [],
        {'parse': []},
    )
    
    yield (
        ['users'],
        {'parse': ['users']},
    )
    yield (
        ['roles'],
        {'parse': ['roles']},
    )
    
    yield (
        ['everyone'],
        {'parse': ['everyone']},
    )
    
    yield (
        ['users', 'roles', 'everyone'],
        {'parse': ['everyone', 'users', 'roles']},
    )
    
    yield (
        [User.precreate(202402170000)],
        {'users': [str(202402170000)]},
    )
    
    yield (
        [User.precreate(202402170001), User.precreate(202402170002)],
        {'users': [str(202402170001), str(202402170002)]},
    )
    
    yield (
        [Role.precreate(202402170003)],
        {'roles': [str(202402170003)]},
    )
    
    yield (
        [Role.precreate(202402170004), Role.precreate(202402170005)],
        {'roles': [str(202402170004), str(202402170005)]},
    )
    
    yield (
        [User.precreate(202402170009), Role.precreate(202402170010)],
        {'users': [str(202402170009)], 'roles': [str(202402170010)]},
    )
    
    yield (
        ['replied_user'],
        {'replied_user': True},
    )
    
    yield (
        ['!replied_user'],
        {'replied_user': False},
    )


@vampytest._(vampytest.call_from(_iter_options__to_data()).returning_last())
def test__AllowedMentionProxy__to_data(parameters):
    """
    Tests whether ``AllowedMentionProxy.to_data`` works as intended.
    
    Parameters
    ----------
    parameters : `list<object>`
        Parameters to create the instance with.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    proxy = AllowedMentionProxy(*parameters)
    return proxy.to_data()



def _iter_options__repr():
    yield (
        [],
        '',
    )
    
    yield (
        ['users'],
        'allow_users = True',
    )
    yield (
        ['roles'],
        'allow_roles = True',
    )
    
    yield (
        ['everyone'],
        'allow_everyone = True',
    )
    
    yield (
        ['users', 'roles', 'everyone'],
        'allow_everyone = True, allow_roles = True, allow_users = True',
    )
    
    yield (
        [User.precreate(202402170020)],
        'allowed_user_ids = [202402170020]',
    )
    
    yield (
        [User.precreate(202402170021), User.precreate(202402170022)],
        'allowed_user_ids = [202402170021, 202402170022]',
    )
    
    yield (
        [Role.precreate(202402170023)],
        'allowed_role_ids = [202402170023]',
    )
    
    yield (
        [Role.precreate(202402170024), Role.precreate(202402170025)],
        'allowed_role_ids = [202402170024, 202402170025]',
    )
    
    yield (
        [User.precreate(202402170029), Role.precreate(202402170030)],
        'allowed_role_ids = [202402170030], allowed_user_ids = [202402170029]',
    )
    
    yield (
        ['replied_user'],
        'allow_replied_user = True',
    )
    
    yield (
        ['!replied_user'],
        'allow_replied_user = False',
    )


@vampytest.call_from(_iter_options__repr())
def test__AllowedMentionProxy__repr(parameters, should_contain):
    """
    Tests whether ``AllowedMentionProxy.__repr__`` works as intended.
    
    Parameters
    ----------
    parameters : `list<object>`
        Parameters to create the instance with.
    """
    proxy = AllowedMentionProxy(*parameters)
    output = repr(proxy)
    vampytest.assert_eq(output, f'<{type(proxy).__name__!s}{" " * bool(should_contain)!s}{should_contain!s}>')


def _iter_options__copy():
    yield (
        [],
    )
    
    yield (
        ['users', 'roles', 'everyone'],
    )

    yield (
        [User.precreate(202402170031), Role.precreate(202402170032)],
    )
    
    yield (
        ['replied_user'],
    )
    
    yield (
        ['!replied_user'],
    )


@vampytest.call_from(_iter_options__copy())
def test__AllowedMentionProxy__repr(parameters):
    """
    Tests whether ``AllowedMentionProxy.copy`` works as intended.
    
    Parameters
    ----------
    parameters : `list<object>`
        Parameters to create the instance with.
    """
    proxy = AllowedMentionProxy(*parameters)
    copy = proxy.copy()
    _assert_fields_set(copy)
    vampytest.assert_eq(proxy, copy)


def _iter_options__eq__true():
    yield (
        [],
        [],
    )
    
    yield (
        ['users', 'roles', 'everyone'],
        ['users', 'roles', 'everyone'],
    )

    yield (
        [User.precreate(202402170033), Role.precreate(202402170034)],
        [User.precreate(202402170033), Role.precreate(202402170034)],
    )
    
    yield (
        ['replied_user'],
        ['replied_user'],
    )
    
    yield (
        ['!replied_user'],
        ['!replied_user'],
    )


def _iter_options__eq__false():
    yield (
        [],
        ['users'],
    )
    
    yield (
        [],
        ['roles'],
    )
    
    yield (
        [],
        ['everyone'],
    )

    yield (
        [],
        [User.precreate(202402170035)],
    )
    
    yield (
        [],
        [Role.precreate(202402170036)],
    )
    
    yield (
        [],
        ['replied_user'],
    )
    
    yield (
        [],
        ['!replied_user'],
    )


@vampytest._(vampytest.call_from(_iter_options__eq__true()).returning(True))
@vampytest._(vampytest.call_from(_iter_options__eq__false()).returning(False))
def test__AllowedMentionProxy__eq(parameters_0, parameters_1):
    """
    Tests whether ``AllowedMentionProxy.copy`` works as intended.
    
    Parameters
    ----------
    parameters_0 : `list<object>`
        Parameters to create the instance with.
    parameters_1 : `list<object>`
        Parameters to create the instance with.
    
    Returns
    -------
    output : `bool`
    """
    proxy_0 = AllowedMentionProxy(*parameters_0)
    proxy_1 = AllowedMentionProxy(*parameters_1)
    output = proxy_0 == proxy_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__hash():
    yield (
        [],
    )
    
    yield (
        ['users', 'roles', 'everyone'],
    )

    yield (
        [User.precreate(202402170037), Role.precreate(202402170038)],
    )
    
    yield (
        ['replied_user'],
    )
    
    yield (
        ['!replied_user'],
    )


@vampytest.call_from(_iter_options__hash())
def test__AllowedMentionProxy__hash(parameters):
    """
    Tests whether ``AllowedMentionProxy.__hash__`` works as intended.
    
    Parameters
    ----------
    parameters : `list<object>`
        Parameters to create the instance with.
    """
    proxy = AllowedMentionProxy(*parameters)
    output = hash(proxy)
    vampytest.assert_instance(output, int)


def _iter_options__and():
    yield (
        [],
        [],
        [],
    )
    
    yield (
        ['users', 'roles', 'everyone'],
        ['users', 'roles', 'everyone'],
        ['users', 'roles', 'everyone'],
    )

    yield (
        [User.precreate(202402170039), Role.precreate(202402170040)],
        [User.precreate(202402170039), Role.precreate(202402170040)],
        [User.precreate(202402170039), Role.precreate(202402170040)],
    )
    
    yield (
        ['replied_user'],
        ['replied_user'],
        ['replied_user'],
    )
    
    yield (
        ['!replied_user'],
        ['!replied_user'],
        ['!replied_user'],
    )
    
    yield (
        [],
        ['users', 'roles', 'everyone'],
        [],
    )

    yield (
        [],
        [User.precreate(202402170041), Role.precreate(202402170042)],
        [],
    )
    
    yield (
        [],
        ['replied_user'],
        [],
    )
    
    yield (
        [],
        ['!replied_user'],
        [],
    )

    yield (
        ['users'],
        ['users', 'roles', 'everyone'],
        ['users'],
    )

    yield (
        ['roles'],
        ['users', 'roles', 'everyone'],
        ['roles'],
    )
    
    yield (
        ['everyone'],
        ['users', 'roles', 'everyone'],
        ['everyone'],
    )
    
    yield (
        [User.precreate(202402170043)],
        [User.precreate(202402170043), Role.precreate(202402170044)],
        [User.precreate(202402170043)],
    )
    
    yield (
        [Role.precreate(202402170045)],
        [User.precreate(202402170046), Role.precreate(202402170045)],
        [Role.precreate(202402170045)],
    )
    
    yield (
        ['users'],
        [User.precreate(202402170047)],
        [User.precreate(202402170047)],
    )
    
    yield (
        ['roles'],
        [Role.precreate(202402170048)],
        [Role.precreate(202402170048)],
    )
    
    yield (
        [Role.precreate(202402170080)],
        [User.precreate(202402170081)],
        [],
    )
    
    yield (
        ['replied_user'],
        ['!replied_user'],
        [],
    )


@vampytest.call_from(_iter_options__and())
def test__AllowedMentionProxy__and(parameters_0, parameters_1, parameters_2):
    """
    Tests whether ``AllowedMentionProxy.and`` works as intended.
    
    Parameters
    ----------
    parameters_0 : `list<object>`
        Parameters to create the instance with.
    parameters_1 : `list<object>`
        Parameters to create the instance with.
    parameters_2 : `list<object>`
        Parameters to create the instance with.
    """
    proxy_0 = AllowedMentionProxy(*parameters_0)
    proxy_1 = AllowedMentionProxy(*parameters_1)
    proxy_2 = AllowedMentionProxy(*parameters_2)
    
    output = proxy_0 & proxy_1
    _assert_fields_set(output)
    vampytest.assert_eq(output, proxy_2)


def test__AllowedMentionProxy__and__not_applicable():
    """
    Tests whether ``AllowedMentionProxy.__and__`` works as intended.
    
    Case: Not applicable for other.
    """
    output = AllowedMentionProxy().__and__('mister')
    vampytest.assert_is(output, NotImplemented)


def _iter_options__xor():
    yield (
        [],
        [],
        [],
    )
    
    yield (
        ['users', 'roles', 'everyone'],
        ['users', 'roles', 'everyone'],
        [],
    )

    yield (
        [User.precreate(202402170059), Role.precreate(202402170060)],
        [User.precreate(202402170059), Role.precreate(202402170060)],
        [],
    )
    
    yield (
        ['replied_user'],
        ['replied_user'],
        [],
    )
    
    yield (
        ['!replied_user'],
        ['!replied_user'],
        [],
    )
    
    yield (
        [],
        ['users', 'roles', 'everyone'],
        ['users', 'roles', 'everyone'],
    )

    yield (
        [],
        [User.precreate(202402170061), Role.precreate(202402170062)],
        [User.precreate(202402170061), Role.precreate(202402170062)],
    )
    
    yield (
        [],
        ['replied_user'],
        ['replied_user'],
    )
    
    yield (
        [],
        ['!replied_user'],
        ['!replied_user'],
    )

    yield (
        ['users'],
        ['users', 'roles', 'everyone'],
        ['roles', 'everyone'],
    )

    yield (
        ['roles'],
        ['users', 'roles', 'everyone'],
        ['users', 'everyone'],
    )
    
    yield (
        ['everyone'],
        ['users', 'roles', 'everyone'],
        ['users', 'roles'],
    )
    
    yield (
        [User.precreate(202402170063)],
        [User.precreate(202402170063), Role.precreate(202402170064)],
        [Role.precreate(202402170064)],
    )
    
    yield (
        [Role.precreate(202402170065)],
        [User.precreate(202402170066), Role.precreate(202402170065)],
        [User.precreate(202402170066)],
    )
    
    yield (
        ['users'],
        [User.precreate(202402170067)],
        ['users'],
    )
    
    yield (
        ['roles'],
        [Role.precreate(202402170068)],
        ['roles'],
    )
    
    yield (
        [Role.precreate(202402170082)],
        [User.precreate(202402170083)],
        [Role.precreate(202402170082), User.precreate(202402170083)],
    )
    
    yield (
        ['replied_user'],
        ['!replied_user'],
        [],
    )


@vampytest.call_from(_iter_options__xor())
def test__AllowedMentionProxy__xor(parameters_0, parameters_1, parameters_2):
    """
    Tests whether ``AllowedMentionProxy.__xor__`` works as intended.
    
    Parameters
    ----------
    parameters_0 : `list<object>`
        Parameters to create the instance with.
    parameters_1 : `list<object>`
        Parameters to create the instance with.
    parameters_2 : `list<object>`
        Parameters to create the instance with.
    """
    proxy_0 = AllowedMentionProxy(*parameters_0)
    proxy_1 = AllowedMentionProxy(*parameters_1)
    proxy_2 = AllowedMentionProxy(*parameters_2)
    
    output = proxy_0 ^ proxy_1
    _assert_fields_set(output)
    vampytest.assert_eq(output, proxy_2)


def test__AllowedMentionProxy__xor__not_applicable():
    """
    Tests whether ``AllowedMentionProxy.__xor__`` works as intended.
    
    Case: Not applicable for other.
    """
    output = AllowedMentionProxy().__xor__('mister')
    vampytest.assert_is(output, NotImplemented)


def _iter_options__or():
    yield (
        [],
        [],
        [],
    )
    
    yield (
        ['users', 'roles', 'everyone'],
        ['users', 'roles', 'everyone'],
        ['users', 'roles', 'everyone'],
    )

    yield (
        [User.precreate(202402170069), Role.precreate(202402170070)],
        [User.precreate(202402170069), Role.precreate(202402170070)],
        [User.precreate(202402170069), Role.precreate(202402170070)],
    )
    
    yield (
        ['replied_user'],
        ['replied_user'],
        ['replied_user'],
    )
    
    yield (
        ['!replied_user'],
        ['!replied_user'],
        ['!replied_user'],
    )
    
    yield (
        [],
        ['users', 'roles', 'everyone'],
        ['users', 'roles', 'everyone'],
    )

    yield (
        [],
        [User.precreate(202402170071), Role.precreate(202402170072)],
        [User.precreate(202402170071), Role.precreate(202402170072)],
    )
    
    yield (
        [],
        ['replied_user'],
        ['replied_user'],
    )
    
    yield (
        [],
        ['!replied_user'],
        ['!replied_user'],
    )

    yield (
        ['users'],
        ['users', 'roles', 'everyone'],
        ['users', 'roles', 'everyone'],
    )

    yield (
        ['roles'],
        ['users', 'roles', 'everyone'],
        ['users', 'roles', 'everyone'],
    )
    
    yield (
        ['everyone'],
        ['users', 'roles', 'everyone'],
        ['users', 'roles', 'everyone'],
    )
    
    yield (
        [User.precreate(202402170073)],
        [User.precreate(202402170073), Role.precreate(202402170074)],
        [User.precreate(202402170073), Role.precreate(202402170074)],
    )
    
    yield (
        [Role.precreate(202402170075)],
        [User.precreate(202402170076), Role.precreate(202402170075)],
        [Role.precreate(202402170075), User.precreate(202402170076)],
    )
    
    yield (
        ['users'],
        [User.precreate(202402170077)],
        ['users'],
    )
    
    yield (
        ['roles'],
        [Role.precreate(202402170078)],
        ['roles'],
    )
    
    yield (
        [Role.precreate(202402170084)],
        [User.precreate(202402170085)],
        [Role.precreate(202402170084), User.precreate(202402170085)],
    )
    
    yield (
        ['replied_user'],
        ['!replied_user'],
        [],
    )


@vampytest.call_from(_iter_options__or())
def test__AllowedMentionProxy__or(parameters_0, parameters_1, parameters_2):
    """
    Tests whether ``AllowedMentionProxy.__or__`` works as intended.
    
    Parameters
    ----------
    parameters_0 : `list<object>`
        Parameters to create the instance with.
    parameters_1 : `list<object>`
        Parameters to create the instance with.
    parameters_2 : `list<object>`
        Parameters to create the instance with.
    """
    proxy_0 = AllowedMentionProxy(*parameters_0)
    proxy_1 = AllowedMentionProxy(*parameters_1)
    proxy_2 = AllowedMentionProxy(*parameters_2)
    
    output = proxy_0 | proxy_1
    _assert_fields_set(output)
    vampytest.assert_eq(output, proxy_2)


def test__AllowedMentionProxy__or__not_applicable():
    """
    Tests whether ``AllowedMentionProxy.__or__`` works as intended.
    
    Case: Not applicable for other.
    """
    output = AllowedMentionProxy().__or__('mister')
    vampytest.assert_is(output, NotImplemented)


def _iter_options__sub():
    yield (
        [],
        [],
        [],
        [],
    )
    
    yield (
        ['users', 'roles', 'everyone'],
        ['users', 'roles', 'everyone'],
        [],
        [],
    )

    yield (
        [User.precreate(202402170090), Role.precreate(202402170091)],
        [User.precreate(202402170090), Role.precreate(202402170091)],
        [],
        [],
    )
    
    yield (
        ['replied_user'],
        ['replied_user'],
        [],
        [],
    )
    
    yield (
        ['!replied_user'],
        ['!replied_user'],
        [],
        [],
    )
    
    yield (
        [],
        ['users', 'roles', 'everyone'],
        [],
        ['users', 'roles', 'everyone'],
    )

    yield (
        [],
        [User.precreate(202402170092), Role.precreate(202402170093)],
        [],
        [User.precreate(202402170092), Role.precreate(202402170093)],
    )
    
    yield (
        [],
        ['replied_user'],
        [],
        ['replied_user'],
    )
    
    yield (
        [],
        ['!replied_user'],
        [],
        ['!replied_user'],
    )

    yield (
        ['users'],
        ['users', 'roles', 'everyone'],
        [],
        ['roles', 'everyone'],
    )

    yield (
        ['roles'],
        ['users', 'roles', 'everyone'],
        [],
        ['users', 'everyone'],
    )
    
    yield (
        ['everyone'],
        ['users', 'roles', 'everyone'],
        [],
        ['users', 'roles'],
    )
    
    yield (
        [User.precreate(202402170094)],
        [User.precreate(202402170094), Role.precreate(202402170095)],
        [],
        [Role.precreate(202402170095)]
    )
    
    yield (
        [Role.precreate(202402170096)],
        [User.precreate(202402170097), Role.precreate(202402170096)],
        [],
        [User.precreate(202402170097)],
    )
    
    yield (
        ['users'],
        [User.precreate(202402170098)],
        ['users'],
        [],
    )
    
    yield (
        ['roles'],
        [Role.precreate(202402170099)],
        ['roles'],
        [],
    )
    
    yield (
        [Role.precreate(202402170100)],
        [User.precreate(202402170102)],
        [Role.precreate(202402170100)],
        [User.precreate(202402170102)],
    )
    
    yield (
        ['replied_user'],
        ['!replied_user'],
        [],
        [],
    )


@vampytest.call_from(_iter_options__sub())
def test__AllowedMentionProxy__sub(parameters_0, parameters_1, parameters_2, parameters_3):
    """
    Tests whether ``AllowedMentionProxy.__sub__`` works as intended.
    
    Parameters
    ----------
    parameters_0 : `list<object>`
        Parameters to create the instance with.
    parameters_1 : `list<object>`
        Parameters to create the instance with.
    parameters_2 : `list<object>`
        Parameters to create the instance with.
    parameters_3 : `list<object>`
        Parameters to create the instance with.
    """
    proxy_0 = AllowedMentionProxy(*parameters_0)
    proxy_1 = AllowedMentionProxy(*parameters_1)
    proxy_2 = AllowedMentionProxy(*parameters_2)
    proxy_3 = AllowedMentionProxy(*parameters_3)
    
    output = proxy_0 - proxy_1
    _assert_fields_set(output)
    vampytest.assert_eq(output, proxy_2)

    output = proxy_1 - proxy_0
    _assert_fields_set(output)
    vampytest.assert_eq(output, proxy_3)


def test__AllowedMentionProxy__sub__not_applicable():
    """
    Tests whether ``AllowedMentionProxy.__sub__`` works as intended.
    
    Case: Not applicable for other.
    """
    output = AllowedMentionProxy().__sub__('mister')
    vampytest.assert_is(output, NotImplemented)

    output = AllowedMentionProxy().__rsub__('mister')
    vampytest.assert_is(output, NotImplemented)



def _iter_options__iter():
    yield (
        [],
    )
    
    yield (
        ['users', 'roles', 'everyone'],
    )

    yield (
        [User.precreate(202402190000), Role.precreate(202402190001)],
    )
    
    yield (
        ['replied_user'],
    )
    
    yield (
        ['!replied_user'],
    )


@vampytest.call_from(_iter_options__iter())
def test__AllowedMentionProxy__iter(parameters):
    """
    Tests whether ``AllowedMentionProxy.__iter__`` works as intended.
    
    Parameters
    ----------
    parameters : `list<object>`
        Parameters to create the instance with.
    
    Returns
    -------
    
    """
    proxy = AllowedMentionProxy(*parameters)
    vampytest.assert_eq({*parameters}, {*proxy})


def _iter_options__update__passing():
    yield (
        [],
        [],
        (0, STATE_ALLOW_REPLIED_USER_NONE, 0, 0, None, None),
    )
    
    yield (
        ['users', 'roles', 'everyone'],
        ['users', 'roles', 'everyone'],
        (1, STATE_ALLOW_REPLIED_USER_NONE, 1, 1, None, None),
    )

    yield (
        [User.precreate(202402190002), Role.precreate(202402190003)],
        [User.precreate(202402190002), Role.precreate(202402190003)],
        (0, STATE_ALLOW_REPLIED_USER_NONE, 0, 0, [202402190003], [202402190002]),
    )
    
    yield (
        ['replied_user'],
        ['replied_user'],
        (0, STATE_ALLOW_REPLIED_USER_TRUE, 0, 0, None, None),
    )
    
    yield (
        ['!replied_user'],
        ['!replied_user'],
        (0, STATE_ALLOW_REPLIED_USER_FALSE, 0, 0, None, None),
    )
    
    yield (
        [],
        ['users', 'roles', 'everyone'],
        (1, STATE_ALLOW_REPLIED_USER_NONE, 1, 1, None, None),
    )

    yield (
        [],
        [User.precreate(202402190004), Role.precreate(202402190005)],
        (0, STATE_ALLOW_REPLIED_USER_NONE, 0, 0, [202402190005], [202402190004]),
    )
    
    yield (
        [],
        ['replied_user'],
        (0, STATE_ALLOW_REPLIED_USER_TRUE, 0, 0, None, None),
    )
    
    yield (
        [],
        ['!replied_user'],
        (0, STATE_ALLOW_REPLIED_USER_FALSE, 0, 0, None, None),
    )

    yield (
        ['users'],
        ['users', 'roles', 'everyone'],
        (1, STATE_ALLOW_REPLIED_USER_NONE, 1, 1, None, None),
    )

    yield (
        ['roles'],
        ['users', 'roles', 'everyone'],
        (1, STATE_ALLOW_REPLIED_USER_NONE, 1, 1, None, None),
    )
    
    yield (
        ['everyone'],
        ['users', 'roles', 'everyone'],
        (1, STATE_ALLOW_REPLIED_USER_NONE, 1, 1, None, None),
    )
    
    yield (
        [User.precreate(202402190006)],
        [User.precreate(202402190006), Role.precreate(202402190007)],
        (0, STATE_ALLOW_REPLIED_USER_NONE, 0, 0, [202402190007], [202402190006]),
    )
    
    yield (
        [Role.precreate(202402190009)],
        [User.precreate(202402190008), Role.precreate(202402190009)],
        (0, STATE_ALLOW_REPLIED_USER_NONE, 0, 0, [202402190009], [202402190008]),
    )
    
    yield (
        ['users'],
        [User.precreate(202402190010)],
        (0, STATE_ALLOW_REPLIED_USER_NONE, 0, 1, None, None),
    )
    
    yield (
        ['roles'],
        [Role.precreate(202402190011)],
        (0, STATE_ALLOW_REPLIED_USER_NONE, 1, 0, None, None),
    )
    
    yield (
        [Role.precreate(202402190012)],
        [User.precreate(202402190013)],
        (0, STATE_ALLOW_REPLIED_USER_NONE, 0, 0, [202402190012], [202402190013]),
    )
    
    yield (
        ['replied_user'],
        ['!replied_user'],
        (0, STATE_ALLOW_REPLIED_USER_FALSE, 0, 0, None, None),
    )
    
    yield (
        ['!replied_user'],
        ['replied_user'],
        (0, STATE_ALLOW_REPLIED_USER_TRUE, 0, 0, None, None),
    )


def _iter_options__update__type_error():
    yield [], [Channel.precreate(202402160006)]
    yield [], [Guild.precreate(202402160006)]
    yield [], [object()]
    yield [], [AllowedMentionProxy('users')]


def _iter_options__update__value_error():
    yield [], ['mister']


@vampytest._(vampytest.call_from(_iter_options__update__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__update__type_error()).raising(TypeError))
@vampytest._(vampytest.call_from(_iter_options__update__value_error()).raising(ValueError))
def test__AllowedMentionProxy__update(parameters_0, parameters_1):
    """
    Tests whether ``AllowedMentionProxy.update`` works as intended.
    
    Parameters
    ----------
    parameters_0 : `list<object>`
        Parameters to create the instance with.
    parameters_1 : `list<object>`
        Parameters to update with.
    
    Returns
    -------
    attributes : `tuple<object>`
    
    Raises
    ------
    TypeError
    ValueError
    """
    proxy = AllowedMentionProxy(*parameters_0)
    proxy_to_update_with = AllowedMentionProxy(*parameters_1)
    
    proxy.update(proxy_to_update_with)
    
    _assert_fields_set(proxy)
    return (
        proxy._allow_everyone,
        proxy._allow_replied_user,
        proxy._allow_roles,
        proxy._allow_users,
        proxy._allowed_role_ids,
        proxy._allowed_user_ids,
    )


def _iter_options__allow_roles__getter():
    yield [], False
    yield ['roles'], True


@vampytest._(vampytest.call_from(_iter_options__allow_roles__getter()).returning_last())
def test__AllowedMentionProxy__allow_roles__getter(parameters):
    """
    Tests whether ``AllowedMentionProxy.allow_roles`` works as intended.
    
    Case: getter.
    
    Parameters
    ----------
    parameters : `list<object>`
        Parameters to create the instance with.
    
    Returns
    -------
    output : `bool`
    """
    proxy = AllowedMentionProxy(*parameters)
    output = proxy.allow_roles
    vampytest.assert_instance(output, bool)
    return output
    

def _iter_options__allow_roles__setter__passing():
    yield False, 0
    yield True, 1


def _iter_options__allow_roles__setter__type_error():
    yield object()
    yield None


@vampytest._(vampytest.call_from(_iter_options__allow_roles__setter__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__allow_roles__setter__type_error()).raising(TypeError))
def test__AllowedMentionProxy__allow_roles__setter(value):
    """
    Tests whether ``AllowedMentionProxy.allow_roles`` works as intended.
    
    Case: setter.
    
    Parameters
    ----------
    value : `object`
        Value to set.
    
    Returns
    -------
    output : `int`
    
    Raises
    ------
    TypeError
    """
    proxy = AllowedMentionProxy()
    proxy.allow_roles = value
    
    output = proxy._allow_roles
    vampytest.assert_instance(output, int)
    return output


def _iter_options__allow_roles__deller():
    yield []
    yield ['roles']


@vampytest._(vampytest.call_from(_iter_options__allow_roles__deller()).returning(0))
def test__AllowedMentionProxy__allow_roles__deller(parameters):
    """
    Tests whether ``AllowedMentionProxy.allow_roles`` works as intended.
    
    Case: deller.
    
    Parameters
    ----------
    parameters : `list<object>`
        Parameters to create the instance with.
    
    Returns
    -------
    output : `int`
    """
    proxy = AllowedMentionProxy(*parameters)
    del proxy.allow_roles
    
    output = proxy._allow_roles
    vampytest.assert_instance(output, int)
    return output


def _iter_options__allow_users__getter():
    yield [], False
    yield ['users'], True


@vampytest._(vampytest.call_from(_iter_options__allow_users__getter()).returning_last())
def test__AllowedMentionProxy__allow_users__getter(parameters):
    """
    Tests whether ``AllowedMentionProxy.allow_users`` works as intended.
    
    Case: getter.
    
    Parameters
    ----------
    parameters : `list<object>`
        Parameters to create the instance with.
    
    Returns
    -------
    output : `bool`
    """
    proxy = AllowedMentionProxy(*parameters)
    output = proxy.allow_users
    vampytest.assert_instance(output, bool)
    return output
    

def _iter_options__allow_users__setter__passing():
    yield False, 0
    yield True, 1


def _iter_options__allow_users__setter__type_error():
    yield object()
    yield None


@vampytest._(vampytest.call_from(_iter_options__allow_users__setter__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__allow_users__setter__type_error()).raising(TypeError))
def test__AllowedMentionProxy__allow_users__setter(value):
    """
    Tests whether ``AllowedMentionProxy.allow_users`` works as intended.
    
    Case: setter.
    
    Parameters
    ----------
    value : `object`
        Value to set.
    
    Returns
    -------
    output : `int`
    
    Raises
    ------
    TypeError
    """
    proxy = AllowedMentionProxy()
    proxy.allow_users = value
    
    output = proxy._allow_users
    vampytest.assert_instance(output, int)
    return output


def _iter_options__allow_users__deller():
    yield []
    yield ['users']


@vampytest._(vampytest.call_from(_iter_options__allow_users__deller()).returning(0))
def test__AllowedMentionProxy__allow_users__deller(parameters):
    """
    Tests whether ``AllowedMentionProxy.allow_users`` works as intended.
    
    Case: deller.
    
    Parameters
    ----------
    parameters : `list<object>`
        Parameters to create the instance with.
    
    Returns
    -------
    output : `int`
    """
    proxy = AllowedMentionProxy(*parameters)
    del proxy.allow_users
    
    output = proxy._allow_users
    vampytest.assert_instance(output, int)
    return output


def _iter_options__allow_everyone__getter():
    yield [], False
    yield ['everyone'], True


@vampytest._(vampytest.call_from(_iter_options__allow_everyone__getter()).returning_last())
def test__AllowedMentionProxy__allow_everyone__getter(parameters):
    """
    Tests whether ``AllowedMentionProxy.allow_everyone`` works as intended.
    
    Case: getter.
    
    Parameters
    ----------
    parameters : `list<object>`
        Parameters to create the instance with.
    
    Returns
    -------
    output : `bool`
    """
    proxy = AllowedMentionProxy(*parameters)
    output = proxy.allow_everyone
    vampytest.assert_instance(output, bool)
    return output
    

def _iter_options__allow_everyone__setter__passing():
    yield False, 0
    yield True, 1


def _iter_options__allow_everyone__setter__type_error():
    yield object()
    yield None


@vampytest._(vampytest.call_from(_iter_options__allow_everyone__setter__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__allow_everyone__setter__type_error()).raising(TypeError))
def test__AllowedMentionProxy__allow_everyone__setter(value):
    """
    Tests whether ``AllowedMentionProxy.allow_everyone`` works as intended.
    
    Case: setter.
    
    Parameters
    ----------
    value : `object`
        Value to set.
    
    Returns
    -------
    output : `int`
    
    Raises
    ------
    TypeError
    """
    proxy = AllowedMentionProxy()
    proxy.allow_everyone = value
    
    output = proxy._allow_everyone
    vampytest.assert_instance(output, int)
    return output


def _iter_options__allow_everyone__deller():
    yield []
    yield ['everyone']


@vampytest._(vampytest.call_from(_iter_options__allow_everyone__deller()).returning(0))
def test__AllowedMentionProxy__allow_everyone__deller(parameters):
    """
    Tests whether ``AllowedMentionProxy.allow_everyone`` works as intended.
    
    Case: deller.
    
    Parameters
    ----------
    parameters : `list<object>`
        Parameters to create the instance with.
    
    Returns
    -------
    output : `int`
    """
    proxy = AllowedMentionProxy(*parameters)
    del proxy.allow_everyone
    
    output = proxy._allow_everyone
    vampytest.assert_instance(output, int)
    return output


@vampytest._(vampytest.call_from(_iter_options__allow_users__deller()).returning(0))
def test__AllowedMentionProxy__allow_users__deller(parameters):
    """
    Tests whether ``AllowedMentionProxy.allow_users`` works as intended.
    
    Case: deller.
    
    Parameters
    ----------
    parameters : `list<object>`
        Parameters to create the instance with.
    
    Returns
    -------
    output : `int`
    """
    proxy = AllowedMentionProxy(*parameters)
    del proxy.allow_users
    
    output = proxy._allow_users
    vampytest.assert_instance(output, int)
    return output


def _iter_options__allow_replied_user__getter():
    yield [], None
    yield ['replied_user'], True
    yield ['!replied_user'], False


@vampytest._(vampytest.call_from(_iter_options__allow_replied_user__getter()).returning_last())
def test__AllowedMentionProxy__allow_replied_user__getter(parameters):
    """
    Tests whether ``AllowedMentionProxy.allow_replied_user`` works as intended.
    
    Case: getter.
    
    Parameters
    ----------
    parameters : `list<object>`
        Parameters to create the instance with.
    
    Returns
    -------
    output : `None | bool`
    """
    proxy = AllowedMentionProxy(*parameters)
    output = proxy.allow_replied_user
    vampytest.assert_instance(output, bool, nullable = True)
    return output
    

def _iter_options__allow_replied_user__setter__passing():
    yield False, STATE_ALLOW_REPLIED_USER_FALSE
    yield True, STATE_ALLOW_REPLIED_USER_TRUE
    yield None, STATE_ALLOW_REPLIED_USER_NONE


def _iter_options__allow_replied_user__setter__type_error():
    yield object()


@vampytest._(vampytest.call_from(_iter_options__allow_replied_user__setter__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__allow_replied_user__setter__type_error()).raising(TypeError))
def test__AllowedMentionProxy__allow_replied_user__setter(value):
    """
    Tests whether ``AllowedMentionProxy.allow_replied_user`` works as intended.
    
    Case: setter.
    
    Parameters
    ----------
    value : `object`
        Value to set.
    
    Returns
    -------
    output : `int`
    
    Raises
    ------
    TypeError
    """
    proxy = AllowedMentionProxy()
    proxy.allow_replied_user = value
    
    output = proxy._allow_replied_user
    vampytest.assert_instance(output, int)
    return output


def _iter_options__allow_replied_user__deller():
    yield []
    yield ['replied_user']
    yield ['!replied_user']


@vampytest._(vampytest.call_from(_iter_options__allow_replied_user__deller()).returning(STATE_ALLOW_REPLIED_USER_NONE))
def test__AllowedMentionProxy__allow_replied_user__deller(parameters):
    """
    Tests whether ``AllowedMentionProxy.allow_replied_user`` works as intended.
    
    Case: deller.
    
    Parameters
    ----------
    parameters : `list<object>`
        Parameters to create the instance with.
    
    Returns
    -------
    output : `int`
    """
    proxy = AllowedMentionProxy(*parameters)
    del proxy.allow_replied_user
    
    output = proxy._allow_replied_user
    vampytest.assert_instance(output, int)
    return output


def _iter_options__allowed_roles__getter():
    role = Role.precreate(202402200000)
    yield [], None
    yield [role], [role]


@vampytest._(vampytest.call_from(_iter_options__allowed_roles__getter()).returning_last())
def test__AllowedMentionProxy__allowed_roles__getter(parameters):
    """
    Tests whether ``AllowedMentionProxy.allowed_roles`` works as intended.
    
    Case: getter.
    
    Parameters
    ----------
    parameters : `list<object>`
        Parameters to create the instance with.
    
    Returns
    -------
    output : `None | list<Role>`
    """
    proxy = AllowedMentionProxy(*parameters)
    output = proxy.allowed_roles
    vampytest.assert_instance(output, list, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, Role)
    
    return output
    

def _iter_options__allowed_roles__setter__passing():
    role = Role.precreate(202402200001)
    yield None, None
    yield role, [role.id]
    yield [], None
    yield [role], [role.id]


def _iter_options__allowed_roles__setter__type_error():
    yield object()


@vampytest._(vampytest.call_from(_iter_options__allowed_roles__setter__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__allowed_roles__setter__type_error()).raising(TypeError))
def test__AllowedMentionProxy__allowed_roles__setter(value):
    """
    Tests whether ``AllowedMentionProxy.allowed_roles`` works as intended.
    
    Case: setter.
    
    Parameters
    ----------
    value : `object`
        Value to set.
    
    Returns
    -------
    output : `list<int>`
    
    Raises
    ------
    TypeError
    """
    proxy = AllowedMentionProxy()
    proxy.allowed_roles = value
    
    output = proxy._allowed_role_ids
    vampytest.assert_instance(output, list, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, int)
    
    return output


def _iter_options__allowed_roles__deller():
    role = Role.precreate(202402200002)
    yield []
    yield [role]


@vampytest._(vampytest.call_from(_iter_options__allowed_roles__deller()).returning(None))
def test__AllowedMentionProxy__allowed_roles__deller(parameters):
    """
    Tests whether ``AllowedMentionProxy.allowed_roles`` works as intended.
    
    Case: deller.
    
    Parameters
    ----------
    parameters : `list<object>`
        Parameters to create the instance with.
    
    Returns
    -------
    output : `None | list<int>`
    """
    proxy = AllowedMentionProxy(*parameters)
    del proxy.allowed_roles
    
    output = proxy._allowed_role_ids
    vampytest.assert_instance(output, list, nullable = True)
    return output



def _iter_options__allowed_users__getter():
    user = User.precreate(202402200004)
    yield [], None
    yield [user], [user]


@vampytest._(vampytest.call_from(_iter_options__allowed_users__getter()).returning_last())
def test__AllowedMentionProxy__allowed_users__getter(parameters):
    """
    Tests whether ``AllowedMentionProxy.allowed_users`` works as intended.
    
    Case: getter.
    
    Parameters
    ----------
    parameters : `list<object>`
        Parameters to create the instance with.
    
    Returns
    -------
    output : `None | list<UserBase>`
    """
    proxy = AllowedMentionProxy(*parameters)
    output = proxy.allowed_users
    vampytest.assert_instance(output, list, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, UserBase)
    
    return output


def _iter_options__allowed_users__setter__passing():
    user = User.precreate(202402200005)
    yield None, None
    yield user, [user.id]
    yield [], None
    yield [user], [user.id]


def _iter_options__allowed_users__setter__type_error():
    yield object()


@vampytest._(vampytest.call_from(_iter_options__allowed_users__setter__passing()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__allowed_users__setter__type_error()).raising(TypeError))
def test__AllowedMentionProxy__allowed_users__setter(value):
    """
    Tests whether ``AllowedMentionProxy.allowed_users`` works as intended.
    
    Case: setter.
    
    Parameters
    ----------
    value : `object`
        Value to set.
    
    Returns
    -------
    output : `list<int>`
    
    Raises
    ------
    TypeError
    """
    proxy = AllowedMentionProxy()
    proxy.allowed_users = value
    
    output = proxy._allowed_user_ids
    vampytest.assert_instance(output, list, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, int)
    
    return output


def _iter_options__allowed_users__deller():
    user = User.precreate(202402200006)
    yield []
    yield [user]


@vampytest._(vampytest.call_from(_iter_options__allowed_users__deller()).returning(None))
def test__AllowedMentionProxy__allowed_users__deller(parameters):
    """
    Tests whether ``AllowedMentionProxy.allowed_users`` works as intended.
    
    Case: deller.
    
    Parameters
    ----------
    parameters : `list<object>`
        Parameters to create the instance with.
    
    Returns
    -------
    output : `None | list<int>`
    """
    proxy = AllowedMentionProxy(*parameters)
    del proxy.allowed_users
    
    output = proxy._allowed_user_ids
    vampytest.assert_instance(output, list, nullable = True)
    return output
