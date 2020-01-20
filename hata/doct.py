# -*- coding: utf-8 -*-
import sys

if (sys.hash_info.width>=64):
    #if we have 64 bit system we can use array instead of list
    from array import array as Array
    def create_array():
        return Array('Q')
else:
    create_array=list
    
if sys.implementation.name=='cpython':
    #on cpython bisect is 4~ times faster.
    import bisect
    _relativeindex=bisect.bisect_left
    del bisect

else:
    def _relativeindex(array,value):
        bot=0
        top=len(array)
        while True:
            if bot<top:
                half=(bot+top)>>1
                if array[half]<value:
                    bot=half+1
                else:
                    top=half
                continue
            break
        return bot

del sys

class DOC_default_id_cont(object):
    __slots__=('_elements', '_ids', '_next',)

    def __init__(self):
        self._elements  = []
        self._ids       = create_array()
        self._next      = 1
    
    def append(self,obj):
        id_=obj.id
        
        if id_<4194304:
            id_=self._next
            obj.id=id_
            self._next=id_+1
            
        array=self._ids
        index=_relativeindex(array,id_)
        
        if index==len(array): #put it at the last place
            array.append(id_)
            self._elements.append(obj)
            return
                
        if array[index]==id_:  #this object is already at the container, lets check it!
            if self._elements[index] is self._elements[index]:
                return
            #hah, got u!
            raise RuntimeError('Two different objects added with same id')


        #insert it at the right place
        array.insert(index,id_)
        self._elements.insert(index,obj)

    def remove(self,obj):
        id_=obj.id
        
        if id_==0:
            return #not in the container

        array=self._ids
        index=_relativeindex(array,id_)

        if index==len(array): #not in the container
            return

        if array[index]!=id_:  #this object is not at the container, lets remove it
            return

        del array[index]
        del self._elements[index]

    #familiar to normal remove
    def remove_by_id(self,id_):
        array=self._ids
        index=_relativeindex(array,id_)

        if index==len(array): #not in the container
            return

        if array[index]!=id_:  #this object is not at the container, lets remove it
            return

        del array[index]
        del self._elements[index]

    def update(self,obj,new_id):
        old_id=obj.id
        obj.id=new_id
        array=self._ids
        old_index=_relativeindex(array,old_id)

        if old_index==len(array) or array[old_index]!=old_id: #not in the container?
            self.append(obj)
            return
        
        new_index=_relativeindex(array,new_id)

        #above or under?
        if old_index<new_index:
            move= 1
            new_index=new_index-1
        elif old_index>new_index:
            move=-1
        else:
            if array[new_index]==new_id:
                #hah, got u!
                raise RuntimeError('Two different objects added with same id')
            return

        #move ids
        index=old_index
        while True:
            if index==new_index:
                break
            array[index]=array[index+move]
            index=index+move
        #put our at the right place
        array[index]=new_id

        elements=self._elements
        #move objest
        index=old_index
        while True:
            if index==new_index:
                break
            elements[index]=elements[index+move]
            index=index+move
        #put our at the right place
        elements[index]=obj

    def __getitem__(self,id_):
        array=self._ids
        index=_relativeindex(array,id_)
        if index==len(array) or array[index]!=id_:
            raise ValueError(f'{id_!r} is not in the {self.__class__.__name__}')
        return self._elements[index]
        
    def __contains__(self,obj):
        id_=obj.id
        array=self._ids
        index=_relativeindex(array,id_)
        if index==len(array):
            return False
        return (array[index]==id_)

    def __len__(self):
        return self._ids.__len__()

    def index(self,obj):
        id_=obj.id
        array=self._ids
        index=_relativeindex(array,id_)
        if index==len(array) or array[index]!=id_:
            raise ValueError(f'{obj!r} is not in the {self.__class__.__name__}')
        return index

    def __iter__(self):
        return self._elements.__iter__()

    def __reversed__(self):
        return self._elements.__reversed__()
    
    def count(self,obj):
        id_=obj.id
        array=self._ids
        index=_relativeindex(array,id_)
        if index==len(array):
            return 0
        if array[index]==id_:
            return 1
        return 0
        
    def copy(self):
        new=list.__new__(type(self))
        new._ids=self._ids.copy()
        new._elements=self._elements.copy()
        new._next=self._next
        return new

    def __repr__(self):
        result=[self.__class__.__name__,'([']
        elements=self._elements
        stop=len(elements)
        if stop:
            stop=stop-1
            index=0
            while index<stop:
                result.append(elements[index].__repr__())
                result.append(', ')
                index=index+1
            result.append(elements[index].__repr__())
        result.append('])')
        
        return ''.join(result)
