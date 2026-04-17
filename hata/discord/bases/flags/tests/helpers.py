from ..flag_deprecation import FlagDeprecation

class FlagDeprecationCountTrigger(FlagDeprecation):
    __slots__ = ('triggered',)
    
    def __new__(cls, use_instead, removed_after, *, trigger_after = None):
        self = FlagDeprecation.__new__(cls, use_instead, removed_after, trigger_after = trigger_after)
        self.triggered = 0
        return self
    
    
    def trigger(self, type_name, flag_name, stack_level):
        self.triggered += 1
        return True
