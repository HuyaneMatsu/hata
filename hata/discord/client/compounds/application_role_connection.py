__all__ = ()

from scarletio import Compound

from ...application import Application, ApplicationRoleConnectionMetadata
from ...http import DiscordHTTPClient

from .application_command import _assert__application_id


class ClientCompoundApplicationRoleConnectionEndpoints(Compound):
    
    application: Application
    http : DiscordHTTPClient
    
    async def application_role_connection_metadata_get_all(self):
        """
        Requests all the role connection metadatas of the client's application.
        
        Returns
        -------
        application_role_connection_metadatas : `list` of `ApplicationRoleConnectionMetadata`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        datas = await self.http.application_role_connection_metadata_get_all(application_id)
        return [ApplicationRoleConnectionMetadata.from_data(data) for data in datas]
    
    
    async def application_role_connection_metadata_edit_all(self, application_role_connection_metadatas):
        """
        Edits all the role connection metadatas of the client's application. Basically overwrites the old ones.
        
        Parameters
        ----------
        application_role_connection_metadatas : `iterable` of ``ApplicationRoleConnectionMetadata``
            The new application connection metadatas to replace the old ones.
        
        Returns
        -------
        application_role_connection_metadatas : `list` of `ApplicationRoleConnectionMetadata`
        
        Raises
        ------
        ConnectionError
            No internet connection.
        DiscordException
            If any exception was received from the Discord API.
        """
        application_id = self.application.id
        assert _assert__application_id(application_id)
        
        datas = [
            application_role_connection_metadata.to_data()
            for application_role_connection_metadata in application_role_connection_metadatas
        ]
        
        datas = await self.http.application_role_connection_metadata_edit_all(application_id, datas)
        return [ApplicationRoleConnectionMetadata.from_data(data) for data in datas]
