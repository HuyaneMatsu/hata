import vampytest

from ....integration import Integration

from ..connection import Connection


def test__Connection__iter_integrations():
    """
    Tests whether ``Connection.iter_integrations` works as intended.
    """
    integration = Integration.precreate(202210080006)
    
    for input_integrations, expected_output in (
        (None, []),
        ([integration], [integration]),
    ):
        connection = Connection(integrations = input_integrations)
        vampytest.assert_eq([*connection.iter_integrations()], expected_output)
