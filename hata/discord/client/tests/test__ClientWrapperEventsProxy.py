import vampytest

from ..client import Client
from ..client_wrapper import ClientWrapper, ClientWrapperEventsProxy


def _assert_fields_set(proxy):
    """
    Tests whether the ``ClientWrapperEventsProxy`` has all of its attribute set.
    
    Parameters
    ----------
    proxy : ``ClientWrapperEventsProxy``
        The proxy to test.
    """
    vampytest.assert_instance(proxy, ClientWrapperEventsProxy)
    vampytest.assert_instance(proxy.called, bool)
    vampytest.assert_instance(proxy.client_wrapper, ClientWrapper)
    vampytest.assert_instance(proxy.keyword_parameters, dict, nullable = True)


def test__ClientWrapperEventsProxy__new():
    """
    Tests whether ``ClientWrapperEventsProxy.__new__`` works as intended.
    """
    called = False
    client_wrapper = ClientWrapper()
    keyword_parameters = {
        'name': 'koishi',
        'overwrite': True,
    }
    
    proxy = ClientWrapperEventsProxy(client_wrapper, called, keyword_parameters)
    _assert_fields_set(proxy)
    
    vampytest.assert_eq(proxy.called, called)
    vampytest.assert_is(proxy.client_wrapper, client_wrapper)
    vampytest.assert_eq(proxy.keyword_parameters, keyword_parameters)


def test__ClientWrapperEventsProxy__call__first():
    """
    Tests whether ``ClientWrapperEventsProxy.__call__`` works as intended.
    
    Case: First call.
    """
    client_wrapper = ClientWrapper()
    
    proxy = ClientWrapperEventsProxy(client_wrapper, False, None)
    
    keyword_parameters = {
        'name': 'koishi',
        'overwrite': True,
    }
    
    output = proxy(**keyword_parameters)
    vampytest.assert_instance(output, ClientWrapperEventsProxy)
    vampytest.assert_eq(output.called, True)
    vampytest.assert_is(output.client_wrapper, client_wrapper)
    vampytest.assert_eq(output.keyword_parameters, keyword_parameters)


def test__ClientWrapperEventsProxy__call__second_without_func():
    """
    Tests whether ``ClientWrapperEventsProxy.__call__`` works as intended.
    
    Case: Second call without `func`.
    """
    client_wrapper = ClientWrapper()
    
    proxy = ClientWrapperEventsProxy(client_wrapper, True, None)
    
    with vampytest.assert_raises(TypeError):
        proxy(None)


def test__ClientWrapperEventsProxy__first_with_func():
    """
    Tests whether ``ClientWrapperEventsProxy.__call__`` works as intended.
    
    Case: First call with `func`.
    """
    client_0 = Client(
        token = 'token_20231124_0000',
        client_id = 202311240000,
        name = 'koishi',
    )
    
    client_1 = Client(
        token = 'token_20231124_0001',
        client_id = 202311240001,
        name = 'satori',
    )
    
    name = 'message_create'
    
    async def func(client, message):
        pass
    
    try:
        proxy = ClientWrapperEventsProxy(ClientWrapper(client_0, client_1), False, None)
        
        proxy(func, name = name)
        
        for client in (client_0, client_1):
            vampytest.assert_is(client.events.message_create, func)
    
    # Cleanup
    finally:
        client = None
        client_0._delete()
        client_0 = None
        client_1._delete()
        client_1 = None


def test__ClientWrapperEventsProxy__second_with_func():
    """
    Tests whether ``ClientWrapperEventsProxy.__call__`` works as intended.
    
    Case: Second call with `func`.
    """
    client_0 = Client(
        token = 'token_20231124_0002',
        client_id = 202311240002,
        name = 'koishi',
    )
    
    client_1 = Client(
        token = 'token_20231124_0003',
        client_id = 202311240003,
        name = 'satori',
    )
    
    name = 'message_create'
    
    async def func(client, message):
        pass
    
    try:
        proxy = ClientWrapperEventsProxy(ClientWrapper(client_0, client_1), True, {'name': name})
        
        proxy(func)
        
        for client in (client_0, client_1):
            vampytest.assert_is(client.events.message_create, func)
    
    # Cleanup
    finally:
        client = None
        client_0._delete()
        client_0 = None
        client_1._delete()
        client_1 = None


def test__ClientWrapperEventsProxy__repr():
    """
    Tests whether ``ClientWrapperEventsProxy.__repr__`` works as intended.
    """
    client_0 = Client(
        token = 'token_20231123_0018',
        client_id = 202311230018,
        name = 'koishi',
    )
    
    client_1 = Client(
        token = 'token_20231123_0019',
        client_id = 202311230019,
        name = 'satori',
    )
    
    keyword_parameters = {
        'name': 'koishi',
        'overwrite': True,
    }
    
    try:
        client_wrapper = ClientWrapper(client_0, client_1)
        
        proxy = ClientWrapperEventsProxy(client_wrapper, True, keyword_parameters)
    
        output = repr(proxy)
        vampytest.assert_instance(output, str)
        
        vampytest.assert_in(ClientWrapperEventsProxy.__name__, output)
        vampytest.assert_in(repr(client_wrapper), output)
    
    # Cleanup
    finally:
        client_0._delete()
        client_0 = None
        client_1._delete()
        client_1 = None


def test__ClientWrapperEventsProxy__eq():
    """
    Tests whether ``ClientWrapperEventsProxy.__eq__`` works as intended.
    """
    client_0 = Client(
        token = 'token_20231123_0020',
        client_id = 202311230020,
        name = 'koishi',
    )
    
    client_1 = Client(
        token = 'token_20231123_0021',
        client_id = 202311230021,
        name = 'satori',
    )
    
    try:
        keyword_parameters = {
            'client_wrapper': ClientWrapper(client_0, client_1),
            'called': False,
            'keyword_parameters': {
                'name': 'koishi',
                'overwrite': True,
            },
        }
        
        proxy = ClientWrapperEventsProxy(**keyword_parameters)
        vampytest.assert_eq(proxy, proxy)
        vampytest.assert_ne(proxy, object())
        
        for field_name, field_value in (
            ('client_wrapper', ClientWrapper(client_0)),
            ('called', True),
            ('keyword_parameters', None)
        ):
            test_proxy = ClientWrapperEventsProxy(**{**keyword_parameters, field_name: field_value})
            vampytest.assert_ne(proxy, test_proxy)
    
    # Cleanup
    finally:
        client_0._delete()
        client_0 = None
        client_1._delete()
        client_1 = None
