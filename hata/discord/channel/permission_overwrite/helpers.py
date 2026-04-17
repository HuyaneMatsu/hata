__all__ = ()

from ....env import API_VERSION


if API_VERSION in (6, 7):
    def get_permission_overwrite_key_value(data):
        """
        Returns the permission overwrite's type's value.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received permission overwrite data.
        
        Returns
        -------
        type_value : `str`
        """
        value = data.get('type', None)
        if value is None:
            value = -1
        return value

else:
    def get_permission_overwrite_key_value(data):
        """
        Returns the permission overwrite's type's value.
        
        Parameters
        ----------
        data : `dict<str, object>`
            Received permission overwrite data.
        
        Returns
        -------
        type_value : `int`
        """
        value = data.get('type', None)
        if value is None:
            value = -1
        else:
            value = int(value)
        return value
