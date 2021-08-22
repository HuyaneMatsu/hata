__all__ = ()

from ...discord.user import User

def handle_dispatch_ready(self, data):
    self.user = User(data['user'])
    
    self._set_connection_waiter_result(True)


DISPATCH_EVENT_HANDLERS = {
    'READY': handle_dispatch_ready,
}

del handle_dispatch_ready
