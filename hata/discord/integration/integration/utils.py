__all__ = ('create_partial_integration_from_id', )

from scarletio import export

from ...core import INTEGRATIONS

from .integration import Integration


@export
def create_partial_integration_from_id(integration_id, role_id = 0):
    """
    Creates an integration with the given id.
    
    If the integration already exists, returns that instead.
    
    Parameters
    ----------
    integration_id : `int`
        The unique identifier number of the integration.
    role_id : `int` = `0`, Optional
        The integration's role's identifier.
    
    Returns
    -------
    integration : ``Integration``
    """
    try:
        integration = INTEGRATIONS[integration_id]
    except KeyError:
        integration = Integration._create_with_role(integration_id, role_id)
        INTEGRATIONS[integration_id] = integration
    
    return integration
