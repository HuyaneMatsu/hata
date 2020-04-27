# -*- coding: utf-8 -*-
from .others import id_to_time

class DiscordEntityMeta(type):
    def __new__(cls, name, parents, attributes, immortal=False):
        final_slots = set()
        
        parent_count = len(parents)
        if parent_count > 0:
            parent = parents[0]
            final_slots.update(getattr(parent,'__slots__',()))
            
            #Sublasses might miss hash!
            if attributes.get('__hash__', None) is None:
                attributes['__hash__'] = parent.__hash__
            
            # Remove weakref to avoid error
            try:
                final_slots.remove('__weakref__')
            except KeyError:
                pass
            
            index = 1
            while index < parent_count:
                parent = parents[index]
                final_slots.update(getattr(parent,f'_{parent.__name__}__slots',()))
                index +=1
        
        final_slots.update(attributes.get('__slots__',()))
        
        if immortal:
            for parent in parents:
                if hasattr(parent,'__weakref__'):
                    break
            else:
                final_slots.add('__weakref__')
        
        final_slots = tuple(sorted(final_slots))
        
        attributes['__slots__'] = final_slots
        
        return type.__new__(cls, name, parents, attributes)

class DiscordEntity(object, metaclass = DiscordEntityMeta):
    __slots__ = ('id', )
    
    @property
    def created_at(self):
        return id_to_time(self.id)
    
    def __hash__(self):
        return self.id
    
    def __gt__(self, other):
        if type(self) is type(other):
            return self.id > other.id
        
        return NotImplemented
    
    def __ge__(self, other):
        if type(self) is type(other):
            return self.id >= other.id
        
        return NotImplemented
    
    def __eq__(self, other):
        if type(self) is type(other):
            return self.id == other.id
        
        return NotImplemented
    
    def __ne__(self, other):
        if type(self) is type(other):
            return self.id != other.id
        
        return NotImplemented
    
    def __le__(self, other):
        if type(self) is type(other):
            return self.id <= other.id
        
        return NotImplemented
    
    def __lt__(self, other):
        if type(self) is type(other):
            return self.id < other.id
        
        return NotImplemented
