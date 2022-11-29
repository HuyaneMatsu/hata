__all__ = (
    'FailingAddress', 'RoutePlannerBase', 'RoutePlannerNanoIP', 'RoutePlannerRotatingIp', 'RoutePlannerRotatingNanoIP'
)

import warnings

from scarletio import RichAttributeErrorBaseType, copy_docs

from ...discord.utils import DATETIME_FORMAT_CODE, unix_time_to_datetime

from .constants import (
    LAVALINK_KEY_ROUTEPLANNER_OBJECT, LAVALINK_KEY_ROUTEPLANNER_OBJECT_BLOCK_INDEX_STRING,
    LAVALINK_KEY_ROUTEPLANNER_OBJECT_CURRENT_ADDRESS, LAVALINK_KEY_ROUTEPLANNER_OBJECT_CURRENT_ADDRESS_INDEX_STRING,
    LAVALINK_KEY_ROUTEPLANNER_OBJECT_FAILING_ADDRESSES, LAVALINK_KEY_ROUTEPLANNER_OBJECT_FAILING_ADDRESS_ADDRESS,
    LAVALINK_KEY_ROUTEPLANNER_OBJECT_FAILING_ADDRESS_UNIX_TIME, LAVALINK_KEY_ROUTEPLANNER_OBJECT_IP_BLOCK,
    LAVALINK_KEY_ROUTEPLANNER_OBJECT_IP_BLOCK_SIZE_STRING, LAVALINK_KEY_ROUTEPLANNER_OBJECT_IP_BLOCK_TYPE,
    LAVALINK_KEY_ROUTEPLANNER_OBJECT_IP_INDEX_STRING, LAVALINK_KEY_ROUTEPLANNER_OBJECT_ROTATE_INDEX_STRING,
    LAVALINK_KEY_ROUTEPLANNER_TYPE, LAVALINK_KEY_ROUTEPLANNER_TYPE_NANO_IP, LAVALINK_KEY_ROUTEPLANNER_TYPE_ROTATING_IP,
    LAVALINK_KEY_ROUTEPLANNER_TYPE_ROTATING_NANO_IP
)


class FailingAddress(RichAttributeErrorBaseType):
    """
    Failed address.
    
    Attributes
    ----------
    address : `str`
        The failed address.
    time : `datetime`
        The time, when the fail occurred.
    """
    __slots__ = ('address', 'time')
    
    def __new__(cls, data):
        """
        Creates a new failing address instance.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Failing address data.
        """
        self = object.__new__(cls)
        self.address = data[LAVALINK_KEY_ROUTEPLANNER_OBJECT_FAILING_ADDRESS_ADDRESS]
        self.time = unix_time_to_datetime(data[LAVALINK_KEY_ROUTEPLANNER_OBJECT_FAILING_ADDRESS_UNIX_TIME])
        return self
    
    def __repr__(self):
        """Returns the failing address's representation."""
        return f'<{self.__class__.__name__} address={self.address!r}, time={self.time:{DATETIME_FORMAT_CODE}}>'


def _route_planner_base_repr_generator(route_planner):
    """
    Representation builder for ``RoutePlannerBase``-s.
    
    Parameters
    ----------
    route_planner : ``RoutePlannerBase``.
        The instance to get representation of.
    
    Yields
    ------
    repr_parts : `list` of `str`
        Repr parts to extend.
    
    Examples
    --------
    
    ```py
    for repr_parts in _route_planner_base_repr_generator(route_planner):
        repr_parts.append('...')
    
    return ''.join(repr_parts)
    ```
    """
    repr_parts = ['<', route_planner.__class__.__name__]
    
    repr_parts.append(' ip_block_type=')
    repr_parts.append(route_planner.ip_block_type)
    
    repr_parts.append(', ip_block_size=')
    repr_parts.append(repr(route_planner.ip_block_size))
    
    yield repr_parts
    
    failing_addresses = route_planner.failing_addresses
    if (failing_addresses is None):
        repr_parts.append(', failing_addresses=[')
        
        length = len(failing_addresses)
        index = 0
        
        while True:
            failing_address = failing_addresses[index]
            repr_parts.append(repr(failing_address))
            
            index += 1
            if index == length:
                break
            
            repr_parts.append(', ')
            continue
        
        repr_parts.append(']')
    
    repr_parts.append('>')


class RoutePlannerBase(RichAttributeErrorBaseType):
    """
    Base class of route planners.
    
    Attributes
    ----------
    failing_addresses : `None`, `tuple` of ``FailingAddress``
        The failed addresses.
    ip_block_size : `int`
        The ip block's size.
    ip_block_type : `str`
        The ip block's type.
    """
    __slots__ = 'failing_addresses', 'ip_block_size', 'ip_block_type'
    
    def __new__(cls, data):
        """
        Creates a new route planner instance from the given data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Route planner data.
        """
        self = object.__new__(cls)
        
        ip_block_data = data[LAVALINK_KEY_ROUTEPLANNER_OBJECT_IP_BLOCK]
        self.ip_block_type = ip_block_data[LAVALINK_KEY_ROUTEPLANNER_OBJECT_IP_BLOCK_TYPE]
        self.ip_block_size = int(ip_block_data[LAVALINK_KEY_ROUTEPLANNER_OBJECT_IP_BLOCK_SIZE_STRING])
        
        failing_address_datas = data[LAVALINK_KEY_ROUTEPLANNER_OBJECT_FAILING_ADDRESSES]
        if failing_address_datas:
            failing_addresses = tuple(
                FailingAddress(failing_address_data) for failing_address_data in failing_address_datas
            )
        else:
            failing_addresses = None
        self.failing_addresses = failing_addresses
        
        return self
    
    def __repr__(self):
        """Returns the route planner's representation."""
        for repr_parts in _route_planner_base_repr_generator(self):
            pass
        
        return ''.join(repr_parts)


class RoutePlannerRotatingIp(RoutePlannerBase):
    """
    Ip rotating route planner.
    
    Attributes
    ----------
    failing_addresses : `None`, `tuple` of ``FailingAddress``
        The failed addresses.
    ip_block_size : `int`
        The ip block's size.
    ip_block_type : `str`
        The ip block's type.
    current_address : `str`
        The currently used ip address.
    ip_index : `int`
        The current offset in the block.
    rotate_index : `int`
        The number of rotations, since the lavalink server was restarted.
    """
    __slots__ = ('current_address', 'ip_index', 'rotate_index')
    
    @copy_docs(RoutePlannerBase.__new__)
    def __new__(cls, data):
        self = RoutePlannerBase.__new__(cls, data)
        self.rotate_index = int(data[LAVALINK_KEY_ROUTEPLANNER_OBJECT_ROTATE_INDEX_STRING])
        self.ip_index = int(data[LAVALINK_KEY_ROUTEPLANNER_OBJECT_IP_INDEX_STRING])
        self.current_address = data[LAVALINK_KEY_ROUTEPLANNER_OBJECT_CURRENT_ADDRESS]
        return self
    
    @copy_docs(RoutePlannerBase.__repr__)
    def __repr__(self):
        for repr_parts in _route_planner_base_repr_generator(self):
            repr_parts.append(', rotate_index=')
            repr_parts.append(repr(self.rotate_index))
            
            repr_parts.append(', ip_index=')
            repr_parts.append(repr(self.ip_index))
            
            repr_parts.append(', current_address=')
            repr_parts.append(repr(self.current_address))
        
        return ''.join(repr_parts)


class RoutePlannerNanoIP(RoutePlannerBase):
    """
    Switches the IP on each clock update and uses the current nanosecond in the offset in the used block. This strategy
    requires at least a (combined) /64 IPv6 block (2⁶⁴ addresses).
    
    Attributes
    ----------
    failing_addresses : `None`, `tuple` of ``FailingAddress``
        The failed addresses.
    ip_block_size : `int`
        The ip block's size.
    ip_block_type : `str`
        The ip block's type.
    current_address_index : `int`
        Representing the current offset in the ip block
    """
    __slots__ = ('current_address_index', )
    
    @copy_docs(RoutePlannerBase.__new__)
    def __new__(cls, data):
        self = RoutePlannerBase.__new__(cls, data)
        self.current_address_index = int(data[LAVALINK_KEY_ROUTEPLANNER_OBJECT_CURRENT_ADDRESS_INDEX_STRING])
        return self
    
    @copy_docs(RoutePlannerBase.__repr__)
    def __repr__(self):
        for repr_parts in _route_planner_base_repr_generator(self):
            repr_parts.append(', current_address_index=')
            repr_parts.append(repr(self.current_address_index))
        
        return ''.join(repr_parts)


class RoutePlannerRotatingNanoIP(RoutePlannerNanoIP):
    """
    Switches the IP on each clock update and uses the current nanosecond in the offset of the used block.

    When a ban occurs, this strategy rotates to the next /64 block as fallback strategy. This strategy requires at
    least a /64 IPv6 CIDR (2⁶⁴ addresses).
    
    Attributes
    ----------
    failing_addresses : `None`, `tuple` of ``FailingAddress``
        The failed addresses.
    ip_block_size : `int`
        The ip block's size.
    ip_block_type : `str`
        The ip block's type.
    current_address_index : `int`
        Representing the current offset in the ip block
    block_index : `int`
        Contains which /64 block ips are chosen. This number increases on each ban.
    """
    __slots__ = ('block_index', )
    
    @copy_docs(RoutePlannerBase.__new__)
    def __new__(cls, data):
        self = RoutePlannerNanoIP.__new__(cls, data)
        self.block_index = int(data[LAVALINK_KEY_ROUTEPLANNER_OBJECT_BLOCK_INDEX_STRING])
        return self
    
    @copy_docs(RoutePlannerBase.__repr__)
    def __repr__(self):
        for repr_parts in _route_planner_base_repr_generator(self):
            repr_parts.append(', current_address_index=')
            repr_parts.append(repr(self.current_address_index))
            
            repr_parts.append(', block_index=')
            repr_parts.append(repr(self.block_index))
            
        return ''.join(repr_parts)

ROUTE_PLANNER_TYPES = {
    LAVALINK_KEY_ROUTEPLANNER_TYPE_ROTATING_IP : RoutePlannerRotatingIp,
    LAVALINK_KEY_ROUTEPLANNER_TYPE_NANO_IP : RoutePlannerNanoIP,
    LAVALINK_KEY_ROUTEPLANNER_TYPE_ROTATING_NANO_IP : RoutePlannerRotatingNanoIP,
}

def get_route_planner(data):
    """
    Tries to get the routeplanner based on it's type.
    
    Parameters
    ----------
    data : `dict` Of (`str`, `Any`) items
        Route planner data.
    
    Returns
    -------
    route_planner : `None`, ``RoutePlannerBase``
    """
    route_planner_type_name = data[LAVALINK_KEY_ROUTEPLANNER_TYPE]
    if route_planner_type_name is None:
        route_planner = None
    else:
        try:
            route_planner_type = ROUTE_PLANNER_TYPES[route_planner_type_name]
        except KeyError:
            warnings.warn(
                f'Undefined route planner type : {route_planner_type_name!r}\nPlease open an issue with this message.',
                RuntimeWarning,
            )
            
            route_planner = None
        
        else:
            route_planner_object_data = data[LAVALINK_KEY_ROUTEPLANNER_OBJECT]
            route_planner = route_planner_type(route_planner_object_data)
    
    return route_planner
