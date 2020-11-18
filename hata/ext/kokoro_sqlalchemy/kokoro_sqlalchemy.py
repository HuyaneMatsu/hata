# -*- coding: utf-8 -*-
__all__ = ('KOKORO_STRATEGY', )

from threading import current_thread

from sqlalchemy import util
from sqlalchemy.engine import Engine
from sqlalchemy.engine.strategies import DefaultEngineStrategy

from ...backend.utils import alchemy_incendiary
from ...backend.executor import ExecutorThread


class KOKOROEngine(object):
    __slots__=('_engine', '_worker',)
    def __init__(self, pool, dialect, u, single_worker=True, **kwargs):
        if single_worker:
            worker = ExecutorThread()
        else:
            worker = None
        self._worker = worker
        self._engine = Engine(pool, dialect, u, **kwargs)
    
    @property
    def uses_single_worker(self):
        """
        Returns whether the engine uses a single worker.
        
        Returns
        -------
        uses_single_worker : `bool`
        """
        return (self._worker is not None)
    
    @property
    def dialect(self):
        return self._engine.dialect
    
    @property
    def _has_events(self):
        return self._engine._has_events
    
    @property
    def logger(self):
        return self._engine.logger
    
    @property
    def _execution_options(self):
        return self._engine._execution_options
    
    def _should_log_info(self):
        return self._engine._should_log_info()
    
    def connect(self):
        return ConnectionCM(self._connect())
    
    async def _connect(self):
        executor = self._worker
        if executor is None:
            executor = current_thread().claim_executor()
        connection = await executor.execute(self._engine.connect)
        return AsyncConnection(connection, executor)
    
    def begin(self, close_with_result=False):
        executor=self._worker
        if executor is None:
            executor = current_thread().claim_executor()
        return EngineTransactionCM(self, close_with_result, executor)
    
    async def execute(self, *args, **kwargs):
        executor = self._worker
        if executor is None:
            executor = current_thread().claim_executor()
        result_proxy = await executor.execute(alchemy_incendiary(self._engine.execute, args, kwargs))
        return AsyncResultProxy(result_proxy, executor)
    
    async def scalar(self, *args, **kwargs):
        executor = self._worker
        if executor is None:
            executor = current_thread().claim_executor()
        result_proxy = await executor.execute(alchemy_incendiary(self._engine.execute, args, kwargs))
        async_result_proxy = AsyncResultProxy(result_proxy, executor)
        return await async_result_proxy.scalar()
    
    async def has_table(self, table_name, schema=None):
        return await current_thread().run_in_executor(alchemy_incendiary(self._engine.has_table, (table_name, schema)))
    
    async def table_names(self, schema=None, connection=None):
        task = alchemy_incendiary(self._engine.table_names, (schema, None if connection else connection._connection))
        executor = self._worker
        if executor is None:
            return await current_thread().run_in_executor(task)
        else:
            return await executor.execute(task)
    
    def __del__(self):
        worker = self._worker
        if (worker is not None):
            self._worker = None
            worker.cancel()


class AsyncConnection(object):
    __slots__=('_connection', 'executor',)
    def __init__(self, connection, executor):
        self._connection = connection
        self.executor = executor
    
    async def execute(self, *args, **kwargs):
        result_proxy = await self.executor.execute(alchemy_incendiary(self._connection.execute, args, kwargs))
        return AsyncResultProxy(result_proxy, self.executor)
    
    async def scalar(self, *args, **kwargs):
        result_proxy = await self.executor.execute(alchemy_incendiary(self._connection.execute, args, kwargs))
        async_result_proxy = AsyncResultProxy(result_proxy, self.executor)
        return await async_result_proxy.scalar()
    
    async def close(self, *args, **kwargs):
        await self.executor.execute(alchemy_incendiary(self._connection.close, args, kwargs))
    
    @property
    def closed(self):
        return self._connection.closed
    
    def begin(self):
        return TransactionCM(self._begin())
    
    async def _begin(self):
        transaction = await self.executor.execute(self._connection.begin)
        return AsyncTransaction(transaction, self.executor)
    
    def begin_nested(self):
        return TransactionCM(self._begin_nested())
    
    async def _begin_nested(self):
        transaction = await self.executor.execute(self._connection.begin_nested)
        return AsyncTransaction(transaction, self.executor)
    
    def in_transaction(self):
        return self._connection.in_transaction()


class AsyncTransaction(object):
    __slots__ = ('_transaction', 'executor',)
    def __init__(self, transaction, executor):
        self._transaction = transaction
        self.executor = executor
    
    async def commit(self):
        return await self.executor.execute(self._transaction.commit)
    
    async def rollback(self):
        return await self.executor.execute(self._transaction.rollback)
    
    async def close(self):
        await self.executor.execute(self._transaction.close)


class AsyncResultProxyIterator(object):
    __slots__ = ('_result_proxy', 'executor',)
    def __init__(self, result_proxy, executor):
        self._result_proxy = result_proxy
        self.executor = executor
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        row = await self.executor.execute(self._result_proxy.fetchone)
        if row is None:
            raise StopAsyncIteration
        return row


class AsyncResultProxy(object):
    __slots__ = ('_result_proxy', 'executor',)
    def __init__(self, result_proxy, executor):
        self._result_proxy = result_proxy
        self.executor = executor
    
    def __aiter__(self):
        return AsyncResultProxyIterator(self._result_proxy, self.executor)
    
    async def fetchone(self):
        return self.executor.execute(self._result_proxy.fetchone)
    
    async def fetchmany(self, size=None):
        return await self.executor.execute(self._result_proxy.fetchmany, size=size)
    
    async def fetchall(self):
        return await self.executor.execute(self._result_proxy.fetchall)
    
    async def scalar(self):
        return await self.executor.execute(self._result_proxy.scalar)
    
    async def first(self):
        return await self.executor.execute(self._result_proxy.first)
    
    async def keys(self):
        return await self.executor.execute(self._result_proxy.keys)
    
    async def close(self):
        return await self.executor.execute(self._result_proxy.close)
    
    @property
    def returns_rows(self):
        return self._result_proxy.returns_rows
    
    @property
    def rowcount(self):
        return self._result_proxy.rowcount
    
    @property
    def inserted_primary_key(self):
        return self._result_proxy.inserted_primary_key


class EngineTransactionCM(object):
    __slots__ = ('_close_with_result', '_context', '_engine', 'executor',)

    def __init__(self, engine, close_with_result, executor):
        self._engine = engine
        self._close_with_result = close_with_result
        self.executor = executor
    
    async def __aenter__(self):
        self._context = await self.executor.execute(
            alchemy_incendiary(self._engine._engine.begin, (self._close_with_result,)))
        return AsyncConnection(self._context.__enter__(), self.executor)
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self.executor.execute(alchemy_incendiary(self._context.__exit__, (exc_type, exc_val, exc_tb),))


class ConnectionCM(object):
    __slots__ = ('result', 'task',)
    def __init__(self, task):
        self.task = task
        self.result = None
        
    def __await__(self):
        return self.task.__await__()
    
    async def __aenter__(self):
        self.result = await self.task
        return self.result
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.result.close()


class TransactionCM(ConnectionCM):
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None and self.result._transaction.is_active:
            try:
                await self.result.commit()
            except:
                with util.safe_reraise():
                    await self.result.rollback()
        else:
            await self.result.rollback()

KOKORO_STRATEGY = 'KOKORO'

class KOKOROEngineStrategy(DefaultEngineStrategy):
    name = KOKORO_STRATEGY
    engine_cls = KOKOROEngine

KOKOROEngineStrategy()

del DefaultEngineStrategy
