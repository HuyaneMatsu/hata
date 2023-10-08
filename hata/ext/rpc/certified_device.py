__all__ = ('CertifiedDevice',)

from uuid import UUID

from ...discord.preconverters import preconvert_preinstanced_type, preconvert_str
from ...discord.utils import is_url

from .preinstanced import DeviceType


class CertifiedDevice:
    """
    Certified device.
    
    Attributes
    ----------
    automatic_gain_control : `bool`
        Whether the device's native automatic gain control is enabled.
        
        > Only applicable for `DeviceType.audio_input` devices.
    echo_cancellation : `bool`
        Whether the device's native echo cancellation is enabled.
        
        > Only applicable for `DeviceType.audio_input` devices.
    hardware_mute : `bool`
        Whether the device is hardware muted.
        
        > Only applicable for `DeviceType.audio_input` devices.
    id : `uuid.UUID`
        The device's Windows (?) UUID.
    model : ``Model``
        Model of the product.
    noise_suppression : `bool`
        Whether the device's native noise suppression is enabled.
        
        > Only applicable for `DeviceType.audio_input` devices.
    related : `None`, `tuple` of ``UUID``
        UUID-s of related devices.
    type : ``DeviceType``
        The type of the device.
    vendor : ``Vendor``
        The hardware's vendor.
    """
    __slots__ = (
        'automatic_gain_control', 'echo_cancellation', 'hardware_mute', 'id', 'model', 'noise_suppression', 'related',
        'type', 'vendor'
    )
    
    def __new__(
        cls,
        type_,
        id_,
        vendor,
        model,
        related,
        *,
        echo_cancellation = False,
        noise_suppression = False,
        automatic_gain_control = False,
        hardware_mute = False,
    ):
        """
        Creates a new certified device.
        
        Parameters
        ----------
        type_ : `str`, ``DeviceType``
            The type of the device.
        id_ : `str`, `uuid.UUID`
            The device's Windows (?) UUID.
        
        vendor : ``Vendor``
            The hardware's vendor.
        model : ``Model``
            Model of the product.
        related : `None`, `str`, ``UUID``, `iterable` of ``UUID``
            UUID-s of related devices.
        echo_cancellation : `bool` = `False`, Optional (Keyword only)
            Whether the device's native echo cancellation is enabled. Defaults to `False`.
            
            > Only applicable for `DeviceType.audio_input` devices.
        noise_suppression : `bool` = `False`, Optional (Keyword only)
            Whether the device's native noise suppression is enabled. Defaults to `False`.
            
            > Only applicable for `DeviceType.audio_input` devices.
        automatic_gain_control : `bool` = `False`, Optional (Keyword only)
            Whether the device's native automatic gain control is enabled. Defaults to `False`.
            
            > Only applicable for `DeviceType.audio_input` devices.
        hardware_mute : `bool` = `False`, Optional (Keyword only)
            Whether the device is hardware muted. Defaults to `False`.
            
            > Only applicable for `DeviceType.audio_input` devices.
        
        Raises
        ------
        TypeError
            - If `type` is neither `str` nor ``DeviceType``.
            - If `id_` is neither `str`, nor `uuid.UUID`.
            - If `related` is neither `None`, `str`, `uuid.UUID`, nor iterable of `str`, `uuid.UUID`.
        ValueError
            - If `id_` is not a valid UUID.
            - If `related` is or contains invalid UUID.
        AssertionError
            - If `vendor` is not ``Vendor``.
            - If `model` is not ``Model``.
            - If `echo_cancellation` is not `bool`.
            - If `noise_suppression` is not `bool`.
            - If `automatic_gain_control` is not `bool`.
            - If `hardware_mute` is not `bool`.
        """
        type_ = preconvert_preinstanced_type(type_, 'type_', DeviceType)
        
        if isinstance(id_, UUID):
            id_ = id_
        elif isinstance(id_, str):
            try:
                id_ = UUID(id_)
            except ValueError:
                raise ValueError(
                    f'`id_` is not a valid `UUID`, got {id_!r}.'
                ) from None
        else:
            raise TypeError(
                f'`id_` can be `{UUID.__name__}`, `str`, got {id_.__class__.__name__}; {id_!r}.'
            )
        
        if __debug__:
            if not isinstance(vendor, Vendor):
                raise AssertionError(
                    f'`vendor` can be `{Vendor.__name__}`, got {vendor.__class__.__name__}; {vendor!r}.'
                )
            
            if not isinstance(model, Model):
                raise AssertionError(
                    f'`model` can be `{Model.__name__}`, got {model.__class__.__name__}; {model!r}.'
                )

        if (related is None):
            related_device_uuids = None
        
        elif isinstance(id_, UUID):
            related_device_uuids = (id_, )
        
        elif isinstance(id_, str):
            try:
                related = UUID(related)
            except ValueError:
                raise ValueError(
                    f'`related` is not a valid `UUID`, got {related!r}.'
                ) from None
            
            
            related_device_uuids = (related, )
        
        else:
            iterator = getattr(type(related), '__iter__', None)
            if iterator is None:
                raise TypeError(
                    f'`related` can be `None`, `str`, `{UUID.__name__}`, `iterable` of '
                    f'`str`, `{UUID.__name__}`, got {related.__class__.__name__}; {related!r}.'
                )
            
            related_device_uuids = set()
            for related_element in iterator(related):
                if isinstance(id_, UUID):
                    pass
                elif isinstance(id_, str):
                    try:
                        related_element = UUID(related_element)
                    except ValueError:
                        raise ValueError(
                            f'`related` contains a not valid `UUID`, got {related_element!r}.'
                        ) from None
                else:
                    raise TypeError(
                        f'`related` can contain `{UUID.__name__}`, `str` elements, got '
                        f'{related_element.__class__.__name__}; {related_element!r}; related={related!r}.'
                    )
            
                related_device_uuids.add(related_element)
            
            if related_device_uuids:
                related_device_uuids = tuple(related_device_uuids)
            else:
                related_device_uuids = None
            
        if __debug__:
            if not isinstance(echo_cancellation, bool):
                raise AssertionError(
                    f'`echo_cancellation` can be `bool`, got {echo_cancellation.__class__.__name__}; '
                    f'{echo_cancellation!r}.'
                )
            
            if not isinstance(noise_suppression, bool):
                raise AssertionError(
                    f'`noise_suppression` can be `bool`, got {noise_suppression.__class__.__name__};'
                    f'{noise_suppression!r}.'
                )
            
            if not isinstance(automatic_gain_control, bool):
                raise AssertionError(
                    f'`automatic_gain_control` can be `bool`, got '
                    f'{automatic_gain_control.__class__.__name__}; {automatic_gain_control!r}.'
                )
            
            if not isinstance(hardware_mute, bool):
                raise AssertionError(
                    f'`echo_cancellation` can be `bool`, got {hardware_mute.__class__.__name__}'
                    f'{echo_cancellation!r}.'
                )
        
        self = object.__new__(cls)
        self.automatic_gain_control = automatic_gain_control
        self.echo_cancellation = echo_cancellation
        self.hardware_mute = hardware_mute
        self.id = id_
        self.model = model
        self.noise_suppression = noise_suppression
        self.related = related_device_uuids
        self.type = type_
        self.vendor = vendor
    
    
    def __repr__(self):
        """Returns the device's representation."""
        # Any better repr ideas?
        return f'<{self.__class__.__name__} of {self.model.name!r}>'
    
    
    def to_data(self):
        """
        Converts the device to json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {
            'id': str(self.id),
            'model': self.model.to_data(),
            'vendor': self.vendor.to_data()
        }
        
        type_ = self.type
        
        data['type'] = type_.value
        
        if type_ is DeviceType.audio_input:
            data['automatic_gain_control'] = self.automatic_gain_control
            data['echo_cancellation'] = self.echo_cancellation
            data['hardware_mute'] = self.hardware_mute
            data['noise_suppression'] = self.noise_suppression
        
        related = self.related
        if related is None:
            related = []
        else:
            related = [str(uuid) for uuid in related]
        data['related'] = related
        
        return data
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new device object from the given json data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Device data.
        
        Returns
        -------
        self : ``CertifiedDevice``
        """
        id_ = UUID(data['id'])
        
        related_data = data['related']
        if related_data:
            related = tuple(UUID(related_value) for related_value in related_data)
        else:
            related = None
        
        
        self = object.__new__(cls)
        self.automatic_gain_control = data.get('automatic_gain_control', False)
        self.echo_cancellation = data.get('echo_cancellation', False)
        self.hardware_mute = data.get('hardware_mute', False)
        self.id = id_
        self.model = Model.from_data(data['model'])
        self.noise_suppression = data.get('noise_suppression', False)
        self.related = related
        self.type = DeviceType.get(data['type'])
        self.vendor = Vendor.from_data(data['vendor'])
        return self


class Vendor:
    """
    Hardware vendor.
    
    Attributes
    ----------
    name : `str`
        Url name of the vendor.
    url : `str`
        Url for the vendor.
    """
    __slots__ = ('name', 'url')
    
    def __new__(cls, name, url):
        """
        Creates a new vendor instance.
        
        Parameters
        ----------
        name : `str`
            The name of the vendor.
        url : `str`
            Url for the vendor.
        
        Raises
        ------
        TypeError
            - If `name` is not `str`.
            - If `url` is not `str`.
        ValueError
            - If `name`'s length is out of the expected range [1:2048].
            - If `url`'s length is out of the expected range [1:2048].
        AssertionError
            If `url` is not `str`.
        """
        name = preconvert_str(name, 'name', 1, 2048)
        url = preconvert_str(url, 'url', 1, 2048)
        
        if __debug__:
            if not is_url(url):
                raise AssertionError(
                    f'`url` is not a valid, got: {url!r}.'
                )
        
        self = object.__new__(cls)
        self.name = name
        self.url = url
        return self
    
    
    def __repr__(self):
        """Returns the vendor's representation."""
        return f'<{self.__class__.__name__} name = {self.name!r}>'
    
    
    def to_data(self):
        """
        Converts the vendor to json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        return {
            'name': self.name,
            'url': self.url,
        }
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new vendor object from the given json data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Vendor data.
        
        Returns
        -------
        self : ``Vendor``
        """
        self = object.__new__(cls)
        self.name = data['name']
        self.url = data['url']
        return self


class Model:
    """
    Model of the product.
    
    Attributes
    ----------
    name : `str`
        Url name of the model.
    url : `str`
        Url for the model.
    """
    __slots__ = ('name', 'url')
    
    def __new__(cls, name, url):
        """
        Creates a new model instance.
        
        Parameters
        ----------
        name : `str`
            The name of the model.
        url : `str`
            Url for the model.
        
        Raises
        ------
        TypeError
            - If `name` is not `str`.
            - If `url` is not `str`.
        ValueError
            - If `name`'s length is out of the expected range [1:2048].
            - If `url`'s length is out of the expected range [1:2048].
        AssertionError
            If `url` is not `str`.
        """
        name = preconvert_str(name, 'name', 1, 2048)
        url = preconvert_str(url, 'url', 1, 2048)
        
        if __debug__:
            if not is_url(url):
                raise AssertionError(
                    f'`url` is not a valid, got: {url!r}.'
                )
        
        self = object.__new__(cls)
        self.name = name
        self.url = url
        return self
    
    
    def __repr__(self):
        """Returns the model's representation."""
        return f'<{self.__class__.__name__} name = {self.name!r}>'
    
    
    def to_data(self):
        """
        Converts the model to json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        return {
            'name': self.name,
            'url': self.url,
        }
    
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new model object from the given json data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Model data.
        
        Returns
        -------
        self : ``Model``
        """
        self = object.__new__(cls)
        self.name = data['name']
        self.url = data['url']
        return self
