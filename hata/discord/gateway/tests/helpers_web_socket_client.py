from scarletio.web_socket import WebSocketClient, WebSocketCommonProtocol


class TestWebSocketClient(WebSocketClient):
    """
    `out_operations` is a list of `tuple<str, object>` -> operation name and parameter(s).
    `in_operations` is a list of `tuple<str, bool, object>` -> operation name, raise and value.
    """
    __slots__ = ('in_operations', 'out_operations', 'url')
    
    async def __new__(cls, loop, url, *, in_operations = None, **keyword_parameters):
        if (in_operations is not None):
            in_operations.reverse()
        
        self = WebSocketCommonProtocol.__new__(cls, loop, '', 0)
        self.in_operations = in_operations
        self.out_operations = []
        self.url = url
        return self
    
    
    async def send(self, data):
        self.out_operations.append(('send', data))
    
    
    async def close(self, close_code):
        self.out_operations.append(('close', close_code))
    
    
    def close_transport(self, force):
        self.out_operations.append(('close_transport', force))
    
    
    def _get_next_in(self, operation_name):
        in_operations = self.in_operations
        if not in_operations:
            raise AssertionError('No more operations expected.')
        
        in_operation_name, in_operation_raise, in_operation_value = in_operations[-1]
        if in_operation_name != operation_name:
            raise AssertionError(f'Expected {in_operation_name!r}, got {operation_name!r}.')
        
        del in_operations[-1]
        
        if in_operation_raise:
            raise in_operation_value
        
        return in_operation_value
    
    
    async def receive(self):
        return self._get_next_in('receive')
    
    
    async def ensure_open(self):
        return self._get_next_in('ensure_open')
