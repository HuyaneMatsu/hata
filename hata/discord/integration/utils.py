__all__ = ('create_partial_integration_from_id', )

from ...backend.export import export

from ..core import INTEGRATIONS
from ..user import ZEROUSER

from .integration_detail import IntegrationDetail
from .integration import Integration
from .integration_account import IntegrationAccount

@export
def create_partial_integration_from_id(integration_id, role=None):
    """
    Creates an integration with the given id.
    
    If the integration already exists, returns that instead.
    
    Parameters
    ----------
    integration_id : `int`
        The unique identifier number of the integration.
    role : ``Role``, Optional
        The role of the integration.
    
    Returns
    -------
    integration : ``Integration``
    """
    try:
        integration = INTEGRATIONS[integration_id]
    except KeyError:
        integration = object.__new__(Integration)
        integration.id = integration_id
        integration.name = ''
        integration.type = ''
        integration.enabled = False
        if role is None:
            detail = None
        else:
            detail = IntegrationDetail.from_role(role)
        integration.detail = detail
        integration.user = ZEROUSER
        integration.account = IntegrationAccount.create_empty()
        integration.application = None
    
    return integration
