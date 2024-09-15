import vampytest

from ...activity_secrets import ActivitySecrets

from ..fields import put_secrets_into


def _iter_options():
    secrets = ActivitySecrets(join = 'hell')
    
    yield (None, False, {})
    yield (None, True, {'secrets': None})
    yield (secrets, False, {'secrets': secrets.to_data()})
    yield (secrets, True, {'secrets': secrets.to_data(defaults = True)})


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_secrets_into(input_value, defaults):
    """
    Tests whether ``put_secrets_into`` is working as intended.
    
    Parameters
    ----------
    input_value : `None | ActivitySecrets`
        Value to serialise.
    defaults : `bool`
        Whether fields with their default value should be included.
    
    Returns
    -------
    output : `dict<str, object>`
    """
    return put_secrets_into(input_value, {}, defaults)
