# -*- coding: utf-8 -*-
__all__ = ('AsyncIO', 'ReuAsyncIO', 'ReuBytesIO', )

import os
from io import BytesIO
from threading import current_thread

from .executor import ExecutorThread
from .dereaddons_local import alchemy_incendiary


class ReuBytesIO(BytesIO):
    __slots__=('_last_OP', '_size')
    
    def __init__(self,):
        self._size=0
        self._last_OP='w'
            
    def write(self,data):
        if self._last_OP=='r':
            BytesIO.seek(self,0)
            self._size=0
            self._last_OP='w'
        
        amount=BytesIO.write(self,data)
        self._size+=amount
        return amount
    
    def read(self,amount=None):
        if self._last_OP=='w':
            self._last_OP='r'
        
        if amount is None:
            amount=self._size-self.tell()
        else:
            readable=self._size-self.tell()
            if amount>readable:
                amount=readable
        
        return BytesIO.read(self,amount)
    
    def close(self):
        self.seek(0)

    def __len__(self):
        return self._size

    def seek(self,offset,whence=os.SEEK_SET):
        if whence==os.SEEK_END:
            return self._size
        
        value=BytesIO.seek(self,offset,whence)
        if value>self._size:
            self._size=value
        
        return value

    def real_close(self):
        BytesIO.close(self)

class AsyncIO(object):
    __slots__=('_executor', '_io',)
    
    async def __new__(cls,*args,**kwargs):
        self=object.__new__(cls)
        self._executor=executor = ExecutorThread()
        self._io = await executor.execute(alchemy_incendiary(open,args,kwargs))
        return self
    
    @classmethod
    def wrap(cls,io):
        self=object.__new__(cls)
        self._io=io
        if io.closed:
            self._executor=None
        else:
            self._executor = current_thread().claim_executor()
        return self
    
    @property
    def buffer(self):
        return self._io.buffer

    def __del__(self):
        executor=self._executor
        if executor is None:
            return
        
        self._io.close()
        executor.release()
        self._executor=None

    close=__del__

    @property
    def closed(self):
        return (self._executor is None)

    async def detach(self):
        executor=self._executor
        if executor is None:
            raise ValueError('I/O operation on closed file.')
        raw = await executor.execute(self._io.detach)
        self._executor=None
        return raw

    async def detach_to_self(self):
        executor=self._executor
        if executor is None:
            raise ValueError('I/O operation on closed file.')
        self._io = await executor.execute(self._io.detach)

    @property
    def encoding(self):
        return self._io.encoding

    @property
    def errors(self):
        return self._io.errors

    def fileno(self):
        return self._io.fileno()

    async def flush(self):
        executor=self._executor
        if executor is None:
            raise ValueError('I/O operation on closed file.')
        return await executor.execute(self._io.flush)
        
    def isatty(self):
        return self._io.isatty()

    @property
    def line_buffering(self):
        return self._io.line_buffering

    @property
    def mode(self):
        return self._io.mode

    @property
    def name(self):
        return self._io.name

    @property
    def newlines(self):
        return self.newlines

    async def read(self,size=-1):
        executor=self._executor
        if executor is None:
            raise ValueError('I/O operation on closed file.')
        return await executor.execute(alchemy_incendiary(self._io.read,(size,),))

    def read1(self,*args):
        executor=self._executor
        if executor is None:
            raise ValueError('I/O operation on closed file.')
        return executor.execute(alchemy_incendiary(self._io.read1,args,))

    @property
    def readable(self):
        return self._io.readable

    async def readinto(self,b):
        executor=self._executor
        if executor is None:
            raise ValueError('I/O operation on closed file.')
        return await executor.execute(alchemy_incendiary(self._io.readinto,(b,),))

    async def readinto1(self,b):
        executor=self._executor
        if executor is None:
            raise ValueError('I/O operation on closed file.')
        return await executor.execute(alchemy_incendiary(self._io.readinto1,(b,),))

    async def readline(self,size=-1):
        executor=self._executor
        if executor is None:
            raise ValueError('I/O operation on closed file.')
        return await executor.execute(alchemy_incendiary(self._io.readline,(size,),))

    async def readlines(self,hint=-1):
        executor=self._executor
        if executor is None:
            raise ValueError('I/O operation on closed file.')
        return await executor.execute(alchemy_incendiary(self._io.readlines,(hint,),))

    async def seek(self,*args):
        executor=self._executor
        if executor is None:
            raise ValueError('I/O operation on closed file.')
        return await executor.execute(alchemy_incendiary(self._io.seek,args,))

    def seekable(self):
        return self._io.seekable()

    async def tell(self):
        executor=self._executor
        if executor is None:
            raise ValueError('I/O operation on closed file.')
        return await executor.execute(self._io.tell)

    async def truncate(self,size=None):
        executor=self._executor
        if executor is None:
            raise ValueError('I/O operation on closed file.')
        return await executor.execute(alchemy_incendiary(self._io.truncate,(size,),))
    
    def writable(self):
        return self._io.writable()

    async def write(self,b):
        executor=self._executor
        if executor is None:
            raise ValueError('I/O operation on closed file.')
        return await executor.execute(alchemy_incendiary(self._io.write,(b,),))
    
    async def writelines(self,lines):
        executor=self._executor
        if executor is None:
            raise ValueError('I/O operation on closed file.')
        return await executor.execute(alchemy_incendiary(self._io.writelines,(lines,),))
    

    def __repr__(self):
        executor=self._executor
        return f'<{self.__class__.__name__} io={self._io}, {"closed" if executor is None else repr(executor)}>'

    __str__=__repr__

    def __enter__(self):
        if self._executor is None:
            raise ValueError('Cant enter an already closed io')
        return self

    def __exit__(self,exc_type,exc_val,exc_tb):
        self.__del__()

    class _AsyncIO_it(object):
        __slots__=('_wrapped',)
        
        def __init__(self,wrapped):
            self._wrapped=wrapped

        def __aiter__(self):
            return self

        async def __anext__(self):
            result = await self._wrapped.readline()
            if result:
                return result
            raise StopAsyncIteration
         
    def __aiter__(self):
        return self._AsyncIO_it(self)

class ReuAsyncIO(AsyncIO):
    __slots__=('_executor', '_io', '_should_seek',)

    async def __new__(cls,path,mode='rb',*args,**kwargs):
        if mode not in ('rb',):
            raise ValueError('This class supports \'rb\' mode only')
        self=object.__new__(cls)
        self._executor=executor = ExecutorThread()
        self._io = await executor.execute(alchemy_incendiary(open,(path,mode,*args),kwargs))
        self._should_seek=False
        return self
    
    def close(self):
        self._should_seek=True

    real_close=AsyncIO.__del__

    @classmethod
    def wrap(cls,io):
        self=object.__new__(cls)
        self._io=io
        if io.closed:
            self._executor=None
        else:
            self._executor = current_thread().claim_executor()
        self._should_seek=False
        return self
    

    async def detach(self):
        executor=self._executor
        if executor is None:
            raise ValueError('I/O operation on closed file.')
        raw = await executor.execute(self._io.detach)
        self._executor=None
        self._should_seek=False
        return raw

    def _seek_and_method(self,name,*args):
        io=self._io
        io.seek(0)
        self._should_seek=False
        return getattr(io,name)(*args)
        
    async def read(self,size=-1):
        executor=self._executor
        if executor is None:
            raise ValueError('I/O operation on closed file.')
        if self._should_seek:
            task=alchemy_incendiary(self._seek_and_method,('read',size,),)
        else:
            task=alchemy_incendiary(self._io.read,(size,),)
        return await executor.execute(task)
        
    def read1(self,*args):
        executor=self._executor
        if executor is None:
            raise ValueError('I/O operation on closed file.')
        if self._should_seek:
            task=alchemy_incendiary(self._io._seek_and_method,('read1',*args,),)
        else:
            task=alchemy_incendiary(self._io.read1,args,)
        return executor.execute(task)

    async def readinto(self,b):
        executor=self._executor
        if executor is None:
            raise ValueError('I/O operation on closed file.')
        if self._should_seek:
            task=alchemy_incendiary(self._io._seek_and_method,('readinto',b,),)
        else:
            task=alchemy_incendiary(self._io.readinto,(b,),)
        return await executor.execute(task)

    async def readinto1(self,b):
        executor=self._executor
        if executor is None:
            raise ValueError('I/O operation on closed file.')
        if self._should_seek:
            task=alchemy_incendiary(self._io._seek_and_method,('readinto1',b,),)
        else:
            task=alchemy_incendiary(self._io.readinto1,(b,),)
        return await executor.execute(task)

    async def readline(self,size=-1):
        executor=self._executor
        if executor is None:
            raise ValueError('I/O operation on closed file.')
        if self._should_seek:
            task=alchemy_incendiary(self._io._seek_and_method,('readline',size,),)
        else:
            task=alchemy_incendiary(self._io.readline,(size,),)
        return await executor.execute(task)

    async def readlines(self,hint=-1):
        executor=self._executor
        if executor is None:
            raise ValueError('I/O operation on closed file.')
        if self._should_seek:
            task=alchemy_incendiary(self._io._seek_and_method,('readlines',hint,),)
        else:
            task=alchemy_incendiary(self._io.readlines,(hint,),)
        return await executor.execute(task)

    async def seek(self,*args):
        executor=self._executor
        if executor is None:
            raise ValueError('I/O operation on closed file.')
        if self._should_seek:
            task=alchemy_incendiary(self._io._seek_and_method,('seek',*args,),)
        else:
            task=alchemy_incendiary(self._io.seek,args,)
        return await executor.execute(task)

    async def tell(self):
        executor=self._executor
        if executor is None:
            raise ValueError('I/O operation on closed file.')
        if self._should_seek:
            await executor.execute(alchemy_incendiary(self._io.seek,(0,),))
            self._should_seek=False
            return 0
        return await executor.execute(self._io.tell)

    class _ReuAsyncIO_it(object):
        __slots__=('_wrapped',)
        
        def __init__(self,wrapped):
            self._wrapped=wrapped

        def __aiter__(self):
            return self

        async def __anext__(self):
            wrapped=self._wrapped
            if wrapped._should_seek:
                await AsyncIO.seek(wrapped)(0)
                wrapped.should_seek=False
            
            result = await wrapped.readline()
            if result:
                return result
            raise StopAsyncIteration
         
    def __aiter__(self):
        return self._ReuAsyncIO_it(self)
    
