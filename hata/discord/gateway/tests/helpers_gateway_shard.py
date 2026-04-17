from scarletio import Future, from_json

from ...core import KOKORO

from ..client_base import DiscordGatewayClientBase


class TestGatewayShard(DiscordGatewayClientBase):
    __slots__ = ('run_end_waiter', 'waiter', 'out_operations', 'in_operations')
    
    def __new__(cls, *, in_operations = None):
        
        if in_operations is not None:
            in_operations.reverse()
        
        self = object.__new__(cls)
        self.waiter = None
        self.run_end_waiter = Future(KOKORO)
        self.out_operations = []
        self.in_operations = in_operations
        return self
    
    
    async def run(self, waiter = None):
        self.waiter = waiter
        return await self.run_end_waiter
    
    
    def set_waiter(self, raise_, value):
        waiter = self.waiter
        if waiter is None:
            raise RuntimeError('no waiter')
        
        if raise_:
            waiter.set_exception_if_pending(value)
        else:
            waiter.set_result_if_pending(value)
    
    
    async def change_voice_state(self, guild_id, channel_id, *, self_deaf = False, self_mute = False):
        self.out_operations.append((
            'change_voice_state',
            (guild_id, channel_id, {'self_deaf': self_deaf, 'self_mute': self_mute}),
        ))

    async def send_as_json(self, data):
        self.out_operations.append((
            'send_as_json',
            data,
        ))
    
    
    async def _send_json(self, data):
        self.out_operations.append((
            'send_as_json',
            from_json(data),
        ))
    
    
    async def terminate(self):
        self.out_operations.append((
            'terminate',
            None,
        ))
    
    
    async def close(self):
        self.out_operations.append((
            'close',
            None,
        ))
    
    
    def abort(self):
        self.out_operations.append((
            'abort',
            None,
        ))
    
    
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
    
    
    @property
    def latency(self):
        return self._get_next_in('latency')

    
    @property
    def kokoro(self):
        return self._get_next_in('kokoro')
