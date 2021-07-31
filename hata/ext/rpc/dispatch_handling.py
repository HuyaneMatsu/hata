__all__ = ()

from ...discord.user import User

def handle_dispatch_READY(self, data):
    self.user = User(data['user'])
    
    self._set_connection_waiter_result(True)


DISPATCH_EVENT_HANDLERS = {
    'READY': handle_dispatch_READY,
}

del handle_dispatch_READY
