import vampytest

from ..client import Client
from ..client_wrapper import ClientWrapper, ClientWrapperEventsProxy


def _assert_fields_set(client_wrapper):
    """
    Asserts whether every fields are set of the given client wrapper.
    
    Parameters
    ----------
    client_wrapper : ``ClientWrapper``
        The client wrapper to check.
    """
    vampytest.assert_instance(client_wrapper, ClientWrapper)
    vampytest.assert_instance(client_wrapper.clients, tuple)
    for client in client_wrapper.clients:
        vampytest.assert_instance(client, Client)


def test__ClientWrapper__new__clients_given():
    """
    Tests whether ``ClientWrapper.__new__`` works as intended.
    
    Case: clients given.
    """
    client_0 = Client(
        token = 'token_20231123_0000',
        client_id = 202311230000,
    )
    
    client_1 = Client(
        token = 'token_20231123_0001',
        client_id = 202311230001,
    )
    
    client_2 = Client(
        token = 'token_20231123_0002',
        client_id = 202311230002,
    )
    
    try:
        client_wrapper = ClientWrapper(client_0, client_1)
        _assert_fields_set(client_wrapper)
        
        vampytest.assert_eq(
            {*client_wrapper.clients},
            {client_0, client_1}
        )
    # Cleanup
    finally:
        client_0._delete()
        client_0 = None
        client_1._delete()
        client_1 = None
        client_2._delete()
        client_2 = None


def test__ClientWrapper__new__auto():
    """
    Tests whether ``ClientWrapper.__new__`` works as intended.
    
    Case: auto client detection.
    """
    client_0 = Client(
        token = 'token_20231123_0003',
        client_id = 202311230003,
    )
    
    client_1 = Client(
        token = 'token_20231123_0004',
        client_id = 202311230004,
    )
    
    client_2 = Client(
        token = 'token_20231123_0005',
        client_id = 202311230005,
    )
    
    try:
        client_wrapper = ClientWrapper()
        _assert_fields_set(client_wrapper)
        
        vampytest.assert_eq(
            {*client_wrapper.clients},
            {client_0, client_1, client_2}
        )
    # Cleanup
    finally:
        client_0._delete()
        client_0 = None
        client_1._delete()
        client_1 = None
        client_2._delete()
        client_2 = None


def test__ClientWrapper__new__type_error():
    """
    Tests whether ``ClientWrapper.__new__`` works as intended.
    
    Case: type error.
    """
    with vampytest.assert_raises(TypeError):
        ClientWrapper(object())


def test__ClientWrapper__repr():
    """
    Tests whether ``ClientWrapper.__repr__`` works as intended.
    """
    client_0 = Client(
        token = 'token_20231123_0006',
        client_id = 202311230006,
        name = 'koishi',
    )
    
    client_1 = Client(
        token = 'token_20231123_0007',
        client_id = 202311230007,
        name = 'satori',
    )

    try:
        client_wrapper = ClientWrapper(client_0, client_1)
        
        output = repr(client_wrapper)
        vampytest.assert_instance(output, str)
        
        vampytest.assert_in(ClientWrapper.__name__, output)
        vampytest.assert_in(client_0.name, output)
        vampytest.assert_in(client_1.name, output)
    
    # Cleanup
    finally:
        client_0._delete()
        client_0 = None
        client_1._delete()
        client_1 = None


def test__ClientWrapper__iter():
    """
    Tests whether ``ClientWrapper.__iter__`` works as intended.
    
    Case: clients given.
    """
    client_0 = Client(
        token = 'token_20231123_0008',
        client_id = 202311230008,
    )
    
    client_1 = Client(
        token = 'token_20231123_0009',
        client_id = 202311230009,
    )

    try:
        client_wrapper = ClientWrapper(client_0, client_1)
        
        vampytest.assert_eq(
            {*client_wrapper},
            {client_0, client_1},
        )
    
    # Cleanup
    finally:
        client_0._delete()
        client_0 = None
        client_1._delete()
        client_1 = None


def test__ClientWrapper__contains():
    """
    Tests whether ``ClientWrapper.__contains__`` works as intended.
    """
    client_0 = Client(
        token = 'token_20231123_0010',
        client_id = 202311230010,
    )
    
    client_1 = Client(
        token = 'token_20231123_0011',
        client_id = 202311230011,
    )
    
    client_2 = Client(
        token = 'token_20231123_0012',
        client_id = 202311230012,
    )
    
    try:
        client_wrapper = ClientWrapper(client_0, client_1)
        _assert_fields_set(client_wrapper)
        
        output = client_0 in client_wrapper
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
        
        output = client_1 in client_wrapper
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
        
        output = client_2 in client_wrapper
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, False)
        
    # Cleanup
    finally:
        client_0._delete()
        client_0 = None
        client_1._delete()
        client_1 = None
        client_2._delete()
        client_2 = None


def test__ClientWrapper__eq():
    """
    Tests whether ``ClientWrapper.__eq__`` works as intended.
    """
    client_0 = Client(
        token = 'token_20231123_0017',
        client_id = 202311230017,
    )
    
    client_1 = Client(
        token = 'token_20231123_0018',
        client_id = 202311230018,
    )
    
    try:
        client_wrapper = ClientWrapper(client_0, client_1)
        vampytest.assert_eq(client_wrapper, client_wrapper)
        vampytest.assert_ne(client_wrapper, object())
        
        test_client_wrapper = ClientWrapper(client_1, client_0)
        vampytest.assert_eq(client_wrapper, test_client_wrapper)
        
        test_client_wrapper = ClientWrapper(client_1)
        vampytest.assert_ne(client_wrapper, test_client_wrapper)
    
    # Cleanup
    finally:
        client_0._delete()
        client_0 = None
        client_1._delete()
        client_1 = None


def test__ClientWrapper__events():
    """
    Tests whether ``ClientWrapper.events`` works as intended.
    """
    client_0 = Client(
        token = 'token_20231123_0022',
        client_id = 202311230022,
    )
    
    client_1 = Client(
        token = 'token_20231123_0023',
        client_id = 202311230023,
    )
    
    keyword_parameters = {
        'name': 'koishi',
        'overwrite': True,
    }
    
    try:
        client_wrapper = ClientWrapper(client_0, client_1)
        
        output = client_wrapper.events
        vampytest.assert_instance(output, ClientWrapperEventsProxy)
        vampytest.assert_eq(output, ClientWrapperEventsProxy(client_wrapper, False, None))
        
    # Cleanup
    finally:
        client_0._delete()
        client_0 = None
        client_1._delete()
        client_1 = None
