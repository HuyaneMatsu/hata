import vampytest
from scarletio import WeakReferer

from ......discord.client import Client
from ......discord.client.compounds.tests.helpers import TestDiscordApiClient
from ......discord.events.handling_helpers import check_name
from ......discord.interaction import InteractionEvent

from ..command_base import CommandBase


def _assert_fields_set(command_base):
    """
    Asserts whether the given instance has all of its fields set.
    
    Parameters
    ----------
    command_base : ``CommandBase``
        The command to checkout.
    """
    vampytest.assert_instance(command_base, CommandBase)
    vampytest.assert_instance(command_base._exception_handlers, list, nullable = True)
    vampytest.assert_instance(command_base._parent_reference, WeakReferer, nullable = True)
    vampytest.assert_instance(command_base.name, str)


class InstantiableCommandBase(CommandBase):
    __slots__ = ()
    
    def __new__(cls, function, name = None, **keyword_parameters):
        name = check_name(function, name)
        self = object.__new__(cls)
        self._exception_handlers = None
        self._parent_reference = None
        self.name = name
        return self


def test__CommandBase__new():
    """
    Tests whether ``CommandBase.__new__`` works as intended.
    """
    function = None
    name = 'yuuka'
    
    with vampytest.assert_raises(NotImplementedError):
        CommandBase(function, name)


def test__CommandBase__repr():
    """
    Tests whether ``CommandBase.__repr__`` works as intended.
    """
    function = None
    name = 'yuuka'
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    command_base = InstantiableCommandBase(function, name)
    command_base.error(exception_handler)
    
    output = repr(command_base)
    vampytest.assert_instance(output, str)
    vampytest.assert_in(type(command_base).__name__, output)
    vampytest.assert_in(f'name = {name!r}', output)
    vampytest.assert_in(f'exception_handlers = {[exception_handler]!r}', output)


def test__CommandBase__hash():
    """
    Tests whether ``CommandBase.__hash__`` works as intended.
    """
    function = None
    name = 'yuuka'
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    command_base = InstantiableCommandBase(function, name)
    command_base.error(exception_handler)
    
    output = hash(command_base)
    vampytest.assert_instance(output, int)


def _iter_options__eq():
    function = None
    name = 'yuuka'
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    keyword_parameters = {
        'function': function,
        'name': name,
    }
    
    yield (
        keyword_parameters,
        (),
        keyword_parameters,
        (),
        True,
    )
    
    yield (
        keyword_parameters,
        (),
        {
            **keyword_parameters,
            'name': 'kazami',
        },
        (),
        False,
    )
    
    yield (
        keyword_parameters,
        (),
        keyword_parameters,
        (exception_handler,),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__CommandBase__eq(keyword_parameters_0, exception_handlers_0, keyword_parameters_1, exception_handlers_1):
    """
    Tests whether ``CommandBase.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    exception_handlers_0 : `tuple<CoroutineFunctionType>`
        Exception handlers to register to the instance.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    exception_handlers_1 : `tuple<CoroutineFunctionType>`
        Exception handlers to register to the instance.
    
    Returns
    -------
    output : `bool`
    """
    command_base_0 = InstantiableCommandBase(**keyword_parameters_0)
    for exception_handler in exception_handlers_0:
        command_base_0.error(exception_handler)
    
    command_base_1 = InstantiableCommandBase(**keyword_parameters_1)
    for exception_handler in exception_handlers_1:
        command_base_1.error(exception_handler)
    
    output = command_base_0 == command_base_1
    vampytest.assert_instance(output, bool)
    return output


def _iter_options__format():
    yield '', str
    yield 'm', CommandBase.mention.fget


@vampytest.call_from(_iter_options__format())
def test__CommandBase__format(code, equal_getter):
    """
    Tests whether ``CommandBase.__format__`` works as intended.
    
    Parameters
    ----------
    code : `str`
        Format code.
    
    equal_getter : `FunctionType`
        A function to create something equal.
    """
    function = None
    name = 'yuuka'
    
    command_base = InstantiableCommandBase(function, name)
    
    output = format(command_base, code)
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, equal_getter(command_base))


async def test__CommandBase__invoke():
    """
    Tests whether ``CommandBase.invoke`` works as intended.
    
    This function is a coroutine.
    """
    function = None
    name = 'yuuka'
    
    command_base = InstantiableCommandBase(function, name)
    
    client_id = 202410170000
    interaction_event_id = 202410170001
    token = 'token_' + str(client_id)
    api = TestDiscordApiClient(False, token)
    
    client = Client(
        token,
        api = api,
        client_id = client_id,
    )
    interaction_event = InteractionEvent.precreate(interaction_event_id)
    
    try:
        await command_base.invoke(client, interaction_event)
        
    finally:
        client._delete()
        client = None


def test__CommandBase__error():
    """
    Tests whether ``CommandBase.error`` works as intended.
    """
    function = None
    name = 'yuuka'
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    command_base = InstantiableCommandBase(function, name)
    command_base.error(exception_handler)
    
    vampytest.assert_eq(command_base._exception_handlers, [exception_handler])


def test__CommandBase__copy():
    """
    Tests whether ``CommandBase.copy`` works as intended.
    """
    function = None
    name = 'yuuka'
    
    async def exception_handler(client, interaction_event, command, exception):
        return
    
    command_base = InstantiableCommandBase(function, name)
    command_base.error(exception_handler)
    copy = command_base.copy()
    _assert_fields_set(copy)
    vampytest.assert_eq(copy, command_base)


def test__CommandBase__mention():
    """
    Tests whether ``CommandBase.mention`` works as intended.
    """
    function = None
    name = 'yuuka'
    
    command_base = InstantiableCommandBase(function, name)
    
    output = command_base.mention
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, '')


def test__CommandBase__mention_at():
    """
    Tests whether ``CommandBase.mention_at`` works as intended.
    """
    function = None
    name = 'yuuka'
    guild_id = 202410170002
    
    command_base = InstantiableCommandBase(function, name)
    
    output = command_base.mention_at(guild_id)
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(output, '')
