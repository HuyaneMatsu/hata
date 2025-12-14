import vampytest

from ....discord.exceptions import DiscordException, ERROR_CODES

from ..command import SlashCommand
from ..exceptions import SlasherSyncError


def _assert_fields_set(exception):
    """
    Asserts whether the given exception has all of its fields set.
    
    Parameters
    ----------
    exception : ``SlasherSyncError``
        The instance to check.
    """
    vampytest.assert_instance(exception, SlasherSyncError)
    vampytest.assert_instance(exception.entity, SlashCommand, nullable = True)


def test__SlasherSyncError__new():
    """
    Tests whether ``SlasherSyncError.__new__`` works as intended.
    """
    entity = SlashCommand(None, 'shrimp')
    cause = DiscordException(None, None, None, None)
    
    exception = SlasherSyncError(entity, cause)
    _assert_fields_set(exception)
    
    vampytest.assert_is(exception.entity, entity)
    vampytest.assert_is(exception.__cause__, cause)


def _iter_options__repr():
    entity = SlashCommand(None, 'shrimp')
    cause_0 = ConnectionError()
    cause_1 = DiscordException(None, None, None, None)
    cause_1.status = 400
    cause_1.code = ERROR_CODES.invalid_form_body
    cause_1.message = 'redirect_uris[0].BASE_TYPE_REQUIRED(\'This field is required\')'
    
    yield (
        None,
        None,
        (
            f'{SlasherSyncError.__name__}'
        ),
    )
    
    yield (
        entity,
        None,
        (
            f'{SlasherSyncError.__name__} while syncing {entity.name}\n'
            f'entity = {entity!r}'
        ),
    )
    
    yield (
        entity,
        cause_0,
        (
            f'{SlasherSyncError.__name__} while syncing {entity.name}\n'
            f'entity = {entity!r}\n'
            f'cause = {type(cause_0).__name__}'
        ),
    )
    
    yield (
        entity,
        cause_1,
        (
            f'{SlasherSyncError.__name__} while syncing {entity.name}\n'
            f'entity = {entity!r}\n'
            f'cause = {type(cause_1).__name__}\n'
            '! This error is due to the application having a null value in its redirect urls !\n'
            '! You have to go to Discord Developer Portal and force update the field by changing it !'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__repr()).returning_last())
def test__SlasherSyncError(entity, cause):
    """
    Tests whether ``SlasherSyncError.__repr__`` works as intended.
    
    Parameters
    ----------
    entity: ``None | SlashCommand``
        The entity, who's sync failed.
    
    cause : `BaseException`
        Source exception.
        
    Returns
    -------
    output : `str`
    """
    exception = SlasherSyncError(entity, cause)
    output = repr(exception)
    vampytest.assert_instance(output, str)
    return output
