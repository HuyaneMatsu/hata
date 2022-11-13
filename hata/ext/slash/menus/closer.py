__all__ = ('Closer', )

from scarletio import CancelledError

from ....discord.component import create_button, create_row

from .helpers import CUSTOM_ID_CANCEL, EMOJI_CANCEL, get_auto_check, top_level_check, top_level_get_timeout
from .menu import Menu


class Closer(Menu):
    
    BUTTON_CANCEL = create_button(emoji = EMOJI_CANCEL, custom_id = CUSTOM_ID_CANCEL)
    
    BUTTONS = create_row(BUTTON_CANCEL)
    
    __slots__ = ('page', 'timeout', 'user_check')
    
    def __init__(self, client, event, page, *, check = ..., timeout = -1.0):
        if check is ...:
            check = get_auto_check(event)
        
        self.page = page
        self.timeout = timeout
        self.user_check = check
    
    
    check = top_level_check
    get_timeout = top_level_get_timeout
    
    async def initial_invoke(self):
        self.content = self.page
        self.components = self.BUTTONS
        self.allowed_mentions = None
    
    async def invoke(self, event):
        interaction = event.interaction
        if interaction == self.BUTTON_CANCEL:
            self.cancel(CancelledError())
        
        return False
