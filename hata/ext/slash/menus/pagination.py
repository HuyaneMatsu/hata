__all__ = ('Pagination', )

from scarletio import CancelledError

from ....discord.component import create_button, create_row

from .helpers import (
    CUSTOM_ID_CANCEL, EMOJI_CANCEL, EMOJI_LEFT, EMOJI_LEFT_2, EMOJI_RIGHT, EMOJI_RIGHT_2, get_auto_check,
    top_level_check, top_level_get_timeout
)
from .menu import Menu


class Pagination(Menu):
    BUTTON_LEFT_2 = create_button(emoji = EMOJI_LEFT_2)
    BUTTON_LEFT = create_button(emoji = EMOJI_LEFT)
    BUTTON_RIGHT = create_button(emoji = EMOJI_RIGHT)
    BUTTON_RIGHT_2 = create_button(emoji = EMOJI_RIGHT_2)
    BUTTON_CANCEL = create_button(emoji = EMOJI_CANCEL, custom_id = CUSTOM_ID_CANCEL)
    
    BUTTONS = create_row(BUTTON_LEFT_2, BUTTON_LEFT, BUTTON_RIGHT, BUTTON_RIGHT_2, BUTTON_CANCEL)
    
    __slots__ = ('page_index', 'pages', 'timeout', 'user_check')
    
    def __init__(self, client, event, pages, *, check = ..., timeout = 300.0):
        if check is ...:
            check = get_auto_check(event)
        
        self.pages = pages
        self.page_index = 0
        self.timeout = timeout
        self.user_check = check
    
    
    check = top_level_check
    get_timeout = top_level_get_timeout

    
    async def initial_invoke(self):
        self.components = self.BUTTONS
        self.allowed_mentions = None
        self.BUTTON_LEFT_2.enabled = False
        self.BUTTON_LEFT.enabled = False
        
        pages = self.pages
        self.content = pages[0]
        if len(pages) == 1:
            self.BUTTON_RIGHT_2.enabled = False
            self.BUTTON_RIGHT.enabled = False
   
    
    async def invoke(self, event):
        interaction = event.interaction
        if interaction == self.BUTTON_CANCEL:
            self.cancel(CancelledError())
            return False
        
        pages_index_limit = len(self.pages) - 1
        
        if interaction == self.BUTTON_LEFT:
            page_index = self.page_index - 1
        elif interaction == self.BUTTON_RIGHT:
            page_index = self.page_index + 1
        elif interaction == self.BUTTON_LEFT_2:
            page_index = 0
        elif interaction == self.BUTTON_RIGHT_2:
            page_index = pages_index_limit
        else:
             return False
        
        if page_index < 0:
            page_index = 0
        elif page_index > pages_index_limit:
            page_index = pages_index_limit
        
        if self.page_index == page_index:
            return False
        
        if page_index == 0:
            self.BUTTON_LEFT_2.enabled = False
            self.BUTTON_LEFT.enabled = False
        else:
            self.BUTTON_LEFT_2.enabled = True
            self.BUTTON_LEFT.enabled = True
        
        if page_index == pages_index_limit:
            self.BUTTON_RIGHT_2.enabled = False
            self.BUTTON_RIGHT.enabled = False
        else:
            self.BUTTON_RIGHT_2.enabled = True
            self.BUTTON_RIGHT.enabled = True
        
        self.page_index = page_index
        self.content = self.pages[page_index]
        return True
