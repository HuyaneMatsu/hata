import vampytest

from ...activity_secrets import ActivitySecrets

from ..fields import parse_secrets


def _iter_options():
    secrets = ActivitySecrets(join = 'hell')
    
    yield ({}, None)
    yield ({'secrets': None}, None)
    yield ({'secrets': secrets.to_data()}, secrets)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_secrets(input_data):
    """
    Tests whether ``parse_secrets`` works as intended.
    
    Parameters
    ----------
    input_data : dict<str, object>`
        Data to parse from.
    
    Returns
    -------
    output : `None | ActivitySecrets`
    """
    output = parse_secrets(input_data)
    vampytest.assert_instance(output, ActivitySecrets, nullable = True)
    return output
