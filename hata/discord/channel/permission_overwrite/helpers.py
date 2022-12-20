__all__ = ()

from ....env import API_VERSION


if API_VERSION in (6, 7):
    def get_permission_overwrite_key_value(data):
        """
        Returns the permission overwrite's type's value.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received permission overwrite data.
        
        Returns
        -------
        type_value : `str`
        """
        return data['type']
else:
    def get_permission_overwrite_key_value(data):
        """
        Returns the permission overwrite's type's value.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received permission overwrite data.
        
        Returns
        -------
        type_value : `int`
        """
        return int(data['type'])
