import vampytest
from scarletio import Task, get_event_loop, skip_ready_cycle

from ....client import Client
from ....http import DiscordApiClient

from ...audit_log import AuditLog
from ...audit_log_change import AuditLogChange
from ...audit_log_entry import AuditLogEntry, AuditLogEntryType

from ..audit_log_iterator import AuditLogIterator


class TestDiscordApiClient(DiscordApiClient):
    __slots__ = ('__dict__',)
    
    async def discord_request(self, handler, method, url, data = None, query = None, headers = None, reason = None):
        raise RuntimeError('Real request during testing.')


def _assert_fields_set(audit_log_iterator):
    """
    Asserts whether every fields are set of an audit log iterator.
    
    Parameters
    ----------
    audit_log_iterator : ``AuditLogIterator``
        Instance to check.
    """
    vampytest.assert_instance(audit_log_iterator, AuditLogIterator)
    vampytest.assert_instance(audit_log_iterator._audit_log_entry_index, int)
    vampytest.assert_instance(audit_log_iterator._audit_log_index, int)
    vampytest.assert_instance(audit_log_iterator._data, dict)
    vampytest.assert_instance(audit_log_iterator._load_one_task, Task, nullable = True)
    vampytest.assert_instance(audit_log_iterator.audit_logs, list)
    vampytest.assert_instance(audit_log_iterator.client, Client)
    vampytest.assert_instance(audit_log_iterator.guild_id, int)
    

def test__AuditLogIterator__new__min_fields():
    """
    Tests whether ``AuditLogIterator.__new__`` works as intended.
    
    Case: minimal amount of fields given.
    """
    client_id = 202407050005
    guild_id = 202407050006
    current_time_as_id = 202407050007
    
    client = Client(
        token = 'token_' + str(client_id),
        client_id = client_id,
    )
    
    def now_as_id_mock():
        nonlocal current_time_as_id
        return current_time_as_id
    
    mocked = vampytest.mock_globals(
        AuditLogIterator.__new__,
        now_as_id = now_as_id_mock,
    )
    
    expected_data = {
        'limit': 100,
        'before': current_time_as_id,
    }
    
    try:
        audit_log_iterator = mocked(AuditLogIterator, client, guild_id)
        _assert_fields_set(audit_log_iterator)
        
        vampytest.assert_eq(audit_log_iterator._data, expected_data)
        
        for key, value in expected_data.items():
            vampytest.assert_instance(audit_log_iterator._data[key], type(value))
        
        vampytest.assert_is(audit_log_iterator.client, client)
        vampytest.assert_eq(audit_log_iterator.guild_id, guild_id)
        
    finally:
        client._delete()
        client = None


def test__AuditLogIterator__new__max_fields():
    """
    Tests whether ``AuditLogIterator.__new__`` works as intended.
    
    Case: Maximal amount of fields given.
    """
    client_id = 202407050008
    guild_id = 202407050009
    current_time_as_id = 202407050010
    entry_type = AuditLogEntryType.guild_update
    user_id = 202407050011
    
    client = Client(
        token = 'token_' + str(client_id),
        client_id = client_id,
    )
    
    def now_as_id_mock():
        nonlocal current_time_as_id
        return current_time_as_id
    
    mocked = vampytest.mock_globals(
        AuditLogIterator.__new__,
        now_as_id = now_as_id_mock,
    )
    
    expected_data = {
        'limit': 100,
        'before': current_time_as_id,
        'action_type': entry_type.value,
        'user_id': str(user_id),
    }
    
    try:
        audit_log_iterator = mocked(AuditLogIterator, client, guild_id, entry_type = entry_type, user_id = user_id)
        _assert_fields_set(audit_log_iterator)
        
        vampytest.assert_eq(audit_log_iterator._data, expected_data)
        
        for key, value in expected_data.items():
            vampytest.assert_instance(audit_log_iterator._data[key], type(value))
        
        vampytest.assert_is(audit_log_iterator.client, client)
        vampytest.assert_eq(audit_log_iterator.guild_id, guild_id)
        
    finally:
        client._delete()
        client = None


async def test__AuditLogIterator__load_one_outer():
    """
    Tests whether ``AuditLogIterator._load_one_outer`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202407050012
    guild_id = 202407050013
    
    audit_log = AuditLog(
        guild_id = guild_id,
        entries = [
            AuditLogEntry.precreate(
                entry_id,
                entry_type = AuditLogEntryType.guild_update,
                changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
                guild_id = guild_id,
            ) for entry_id in range(202407050014, 202407050114)
        ],
    )
    
    async def mock_audit_log_get_chunk(input_guild_id, input_data):
        nonlocal guild_id
        nonlocal audit_log
        
        vampytest.assert_eq(input_guild_id, guild_id)
        vampytest.assert_instance(input_data, dict)
        
        await skip_ready_cycle()
        
        return audit_log.to_data()
    
    
    api = TestDiscordApiClient(True, 'token_' + str(client_id))
    api.audit_log_get_chunk = mock_audit_log_get_chunk
    
    client = Client(
        token = 'token_' + str(client_id),
        api = api,
        client_id = client_id,
    )
    
    try:
        audit_log_iterator = AuditLogIterator(client, guild_id)
        old_data = audit_log_iterator._data.copy()
        
        loop = get_event_loop()
        task_0 = loop.create_task(audit_log_iterator._load_one_outer())
        task_1 = loop.create_task(audit_log_iterator._load_one_outer())
        
        task_0.apply_timeout(0.1)
        task_1.apply_timeout(0.1)
        
        output_0 = await task_0
        output_1 = await task_1
        
        vampytest.assert_instance(output_0, bool)
        vampytest.assert_eq(output_0, True)
        vampytest.assert_instance(output_1, bool)
        vampytest.assert_eq(output_1, True)
        
        new_data = audit_log_iterator._data.copy()
        vampytest.assert_ne(old_data, new_data)
        
        vampytest.assert_eq(audit_log_iterator. audit_logs, [audit_log])
        
    finally:
        client._delete()
        client = None


async def test__AuditLogIterator__load_all():
    """
    Tests whether ``AuditLogIterator._load_one_outer`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202407050115
    guild_id = 202407050116
    
    audit_log_0 = AuditLog(
        guild_id = guild_id,
        entries = [
            AuditLogEntry.precreate(
                entry_id,
                entry_type = AuditLogEntryType.guild_update,
                changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
                guild_id = guild_id,
            ) for entry_id in range(202407050117, 202407050217)
        ],
    )
    
    audit_log_1 = AuditLog(
        guild_id = guild_id,
        entries = [
            AuditLogEntry.precreate(
                entry_id,
                entry_type = AuditLogEntryType.guild_update,
                changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
                guild_id = guild_id,
            ) for entry_id in range(202407050217, 202407050219)
        ],
    )
    
    iterator = iter([audit_log_0, audit_log_1])
    
    
    async def mock_audit_log_get_chunk(input_guild_id, input_data):
        nonlocal guild_id
        nonlocal iterator
        
        vampytest.assert_eq(input_guild_id, guild_id)
        vampytest.assert_instance(input_data, dict)
        
        audit_log = next(iterator, None)
        if audit_log is None:
            raise RuntimeError
        
        return audit_log.to_data()
    
    
    api = TestDiscordApiClient(True, 'token_' + str(client_id))
    api.audit_log_get_chunk = mock_audit_log_get_chunk
    
    client = Client(
        token = 'token_' + str(client_id),
        api = api,
        client_id = client_id,
    )
    
    try:
        audit_log_iterator = AuditLogIterator(client, guild_id)
        
        await audit_log_iterator.load_all()
        
        vampytest.assert_eq(audit_log_iterator. audit_logs, [audit_log_0, audit_log_1])
        
    finally:
        client._delete()
        client = None


def test__AuditLogIterator__transform():
    """
    Tests whether ``AuditLogIterator.transform`` works as intended.
    """
    client_id = 202407050220
    guild_id = 202407050221
    
    client = Client(
        token = 'token_' + str(client_id),
        client_id = client_id,
    )
    
    audit_log_0 = AuditLog(
        guild_id = guild_id,
        entries = [
            AuditLogEntry.precreate(
                entry_id,
                entry_type = AuditLogEntryType.guild_update,
                changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
                guild_id = guild_id,
            ) for entry_id in range(202407050222, 202407050223)
        ],
    )
    
    audit_log_1 = AuditLog(
        guild_id = guild_id,
        entries = [
            AuditLogEntry.precreate(
                entry_id,
                entry_type = AuditLogEntryType.guild_update,
                changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
                guild_id = guild_id,
            ) for entry_id in range(202407050223, 202407050224)
        ],
    )
    
    try:
        audit_log_iterator = AuditLogIterator(client, guild_id)
        audit_log_iterator.audit_logs.append(audit_log_0)
        audit_log_iterator.audit_logs.append(audit_log_1)
        
        output = audit_log_iterator.transform()
        vampytest.assert_instance(output, AuditLog)
        
        vampytest.assert_eq(output.guild_id, guild_id)
        vampytest.assert_eq(output.entries, [*audit_log_0.iter_entries(), *audit_log_1.iter_entries()])
        
    finally:
        client._delete()
        client = None


async def test__AuditLogIterator__aiter():
    """
    Tests whether ``AuditLogIterator.__aiter__`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202407050225
    guild_id = 202407050226
    
    audit_log_0 = AuditLog(
        guild_id = guild_id,
        entries = [
            AuditLogEntry.precreate(
                entry_id,
                entry_type = AuditLogEntryType.guild_update,
                changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
                guild_id = guild_id,
            ) for entry_id in range(202407050227, 202407050327)
        ],
    )
    
    audit_log_1 = AuditLog(
        guild_id = guild_id,
        entries = [
            AuditLogEntry.precreate(
                entry_id,
                entry_type = AuditLogEntryType.guild_update,
                changes = [AuditLogChange('name', before = 'okuu', after = 'orin')],
                guild_id = guild_id,
            ) for entry_id in range(202407050327, 202407050329)
        ],
    )
    
    iterator = iter([audit_log_0, audit_log_1])
    
    
    async def mock_audit_log_get_chunk(input_guild_id, input_data):
        nonlocal guild_id
        nonlocal iterator
        
        vampytest.assert_eq(input_guild_id, guild_id)
        vampytest.assert_instance(input_data, dict)
        
        audit_log = next(iterator, None)
        if audit_log is None:
            raise RuntimeError
        
        return audit_log.to_data()
    
    
    api = TestDiscordApiClient(True, 'token_' + str(client_id))
    api.audit_log_get_chunk = mock_audit_log_get_chunk
    
    client = Client(
        token = 'token_' + str(client_id),
        api = api,
        client_id = client_id,
    )
    
    try:
        audit_log_iterator = AuditLogIterator(client, guild_id)
        
        entries = []
        
        async for entry in audit_log_iterator:
            entries.append(entry)
        
        vampytest.assert_eq(entries, [*audit_log_0.iter_entries(), *audit_log_1.iter_entries()])
        
    finally:
        client._delete()
        client = None


def test__AuditLogIterator__repr():
    """
    Tests whether ``AuditLogIterator.__repr__`` works as intended.
    """
    client_id = 202407050330
    guild_id = 202407050331
    
    client = Client(
        token = 'token_' + str(client_id),
        client_id = client_id,
    )
    
    try:
        audit_log_iterator = AuditLogIterator(client, guild_id)
        
        output = repr(audit_log_iterator)
        vampytest.assert_instance(output, str)
        
    finally:
        client._delete()
        client = None
