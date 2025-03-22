__all__ = ('KOKORO_STRATEGY', )

from threading import current_thread

from scarletio import ExecutorThread, alchemy_incendiary
from sqlalchemy import util
from sqlalchemy.engine import Engine
from sqlalchemy.engine.strategies import DefaultEngineStrategy


class KOKOROEngine:
    __slots__ = ('_engine', '_worker',)
    
    def __init__(self, pool, dialect, u, single_worker = True, **keyword_parameters):
        if single_worker:
            worker = ExecutorThread()
        else:
            worker = None
        self._worker = worker
        self._engine = Engine(pool, dialect, u, **keyword_parameters)
    
    
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
        return ConnectionContextManager(self._connect())
    
    
    async def _connect(self):
        executor = self._worker
        if executor is not None:
            release_executor_after = False
        
        else:
            release_executor_after = True
            executor = current_thread().claim_executor()
        
        try:
            connection = await executor.execute(self._engine.connect)
        except:
            if release_executor_after:
                executor.release()
            raise
        
        return AsyncConnection(connection, executor, release_executor_after)
    
    
    def begin(self, close_with_result = False):
        executor = self._worker
        if executor is not None:
            release_executor_after = False
        
        else:
            release_executor_after = True
            executor = current_thread().claim_executor()
        
        return EngineTransactionContextManager(self, close_with_result, executor, release_executor_after)
    
    
    async def execute(self, *positional_parameters, **keyword_parameters):
        executor = self._worker
        if executor is not None:
            release_executor_after = False
        
        else:
            release_executor_after = True
            executor = current_thread().claim_executor()
        
        try:
            result_proxy = await executor.execute(alchemy_incendiary(
                self._engine.execute, positional_parameters, keyword_parameters,
            ))
        except:
            if release_executor_after:
                executor.release()
            raise
        
        return AsyncResultProxy(result_proxy, executor, release_executor_after)
    
    
    async def scalar(self, *positional_parameters, **keyword_parameters):
        executor = self._worker
        if executor is not None:
            release_executor_after = False
        
        else:
            release_executor_after = True
            executor = current_thread().claim_executor()
        
        
        try:
            result_proxy = await executor.execute(alchemy_incendiary(
                self._engine.execute, positional_parameters, keyword_parameters,
            ))
        except:
            if release_executor_after:
                executor.release()
            raise
        
        async_result_proxy = AsyncResultProxy(result_proxy, executor, release_executor_after)
        return await async_result_proxy.scalar()
    
    
    async def has_table(self, table_name, schema = None):
        executor = self._worker
        if executor is not None:
            release_executor_after = False
        
        else:
            release_executor_after = True
            executor = current_thread().claim_executor()
        
        
        try:
            return executor.execute(alchemy_incendiary(self._engine.has_table, (table_name, schema)))
        finally:
            if release_executor_after:
                executor.release()
    
    
    async def table_names(self, schema = None, connection = None):
        executor = self._worker
        if executor is not None:
            release_executor_after = False
        
        else:
            release_executor_after = True
            executor = current_thread().claim_executor()
        
        try:
            return executor.execute(alchemy_incendiary(
                self._engine.table_names, (schema, None if connection else connection._connection)
            ))
        finally:
            if release_executor_after:
                executor.release()
    
    
    def __del__(self):
        worker = self._worker
        if (worker is not None):
            self._worker = None
            worker.cancel()


class AsyncConnection:
    __slots__ = ('_connection', '_release_executor_after', 'executor',)
    
    def __new__(cls, connection, executor, release_executor_after):
        self = object.__new__(cls)
        self._connection = connection
        self._release_executor_after = release_executor_after
        self.executor = executor
        return self
    
    
    async def execute(self, *positional_parameters, **keyword_parameters):
        result_proxy = await self.executor.execute(alchemy_incendiary(
            self._connection.execute, positional_parameters, keyword_parameters,
        ))
        return AsyncResultProxy(result_proxy, self.executor, False)
    
    
    async def scalar(self, *positional_parameters, **keyword_parameters):
        result_proxy = await self.executor.execute(alchemy_incendiary(
            self._connection.execute, positional_parameters, keyword_parameters,
        ))
        async_result_proxy = AsyncResultProxy(result_proxy, self.executor, False)
        return await async_result_proxy.scalar()
    
    
    async def close(self, *positional_parameters, **keyword_parameters):
        await self.executor.execute(alchemy_incendiary(
            self._connection.close, positional_parameters, keyword_parameters
        ))
    
    
    @property
    def closed(self):
        return self._connection.closed
    
    
    def begin(self):
        return TransactionContextManager(self._begin())
    
    
    async def _begin(self):
        transaction = await self.executor.execute(self._connection.begin)
        return AsyncTransaction(transaction, self.executor)
    
    
    def begin_nested(self):
        return TransactionContextManager(self._begin_nested())
    
    
    async def _begin_nested(self):
        transaction = await self.executor.execute(self._connection.begin_nested)
        return AsyncTransaction(transaction, self.executor)
    
    
    def in_transaction(self):
        return self._connection.in_transaction()
    
    
    def __del__(self):
        if self._release_executor_after:
            self.executor.release()


class AsyncTransaction:
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


class AsyncResultProxyIterator:
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


class AsyncResultProxy:
    __slots__ = ('_release_executor_after', '_result_proxy', 'executor',)
    
    def __new__(cls, result_proxy, executor, release_executor_after):
        self = object.__new__(cls)
        self._release_executor_after = release_executor_after
        self._result_proxy = result_proxy
        self.executor = executor
        return self
    
    
    def __aiter__(self):
        return AsyncResultProxyIterator(self._result_proxy, self.executor)
    
    
    async def fetchone(self):
        return await self.executor.execute(self._result_proxy.fetchone)
    
    
    async def fetchmany(self, size = None):
        return await self.executor.execute(self._result_proxy.fetchmany, size = size)
    
    
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
    
    
    def __del__(self):
        if self._release_executor_after:
            self.executor.release()


class EngineTransactionContextManager:
    __slots__ = ('_close_with_result', '_context', '_engine', '_release_executor_after', 'connector', 'executor',)

    def __new__(cls, engine, close_with_result, executor, release_executor_after):
        self = object.__new__(cls)
        self._close_with_result = close_with_result
        self._context = None
        self._engine = engine
        self._release_executor_after = release_executor_after
        self.executor = executor
        return self
    
    
    async def __aenter__(self):
        self._context = await self.executor.execute(
            alchemy_incendiary(self._engine._engine.begin, (self._close_with_result,))
        )
        return AsyncConnection(self._context.__enter__(), self.executor, False)
    
    
    async def __aexit__(self, exception_type, exception_value, exception_traceback):
        return await self.executor.execute(
            alchemy_incendiary(self._context.__exit__, (exception_type, exception_value, exception_traceback),)
        )
    
    
    def __del__(self):
        if self._release_executor_after:
            self.executor.release()


class ConnectionContextManager:
    __slots__ = ('result', 'task',)
    
    def __init__(self, task):
        self.task = task
        self.result = None
        
        
    def __await__(self):
        return self.task.__await__()
    
    
    async def __aenter__(self):
        self.result = await self.task
        return self.result
    
    
    async def __aexit__(self, exception_type, exception_value, exception_traceback):
        await self.result.close()


class TransactionContextManager(ConnectionContextManager):
    __slots__ = ()
    
    async def __aexit__(self, exception_type, exception_value, exception_traceback):
        if exception_type is None and self.result._transaction.is_active:
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
