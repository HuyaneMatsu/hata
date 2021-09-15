__all__ = ('ComponentBase', 'ComponentButton', 'ComponentRow', 'ComponentSelect', 'ComponentSelectOption',
    'create_auto_custom_id', 'create_component')

from os import urandom as random_bytes
from base64 import b85encode as to_base85
import reprlib

from ...backend.utils import copy_docs
from ...backend.export import export

from ..bases import PreinstancedBase
from ..preconverters import preconvert_preinstanced_type
from ..utils import url_cutter
from ..emoji import create_partial_emoji_from_data, Emoji, create_partial_emoji_data

from .preinstanced import ComponentType, ButtonStyle

COMPONENT_TYPE_ROW = ComponentType.row
COMPONENT_TYPE_BUTTON = ComponentType.button
COMPONENT_TYPE_SELECT = ComponentType.select

COMPONENT_SUB_COMPONENT_LIMIT = 5
COMPONENT_LABEL_LENGTH_MAX = 80
COMPONENT_CUSTOM_ID_LENGTH_MAX = 100
COMPONENT_OPTION_LENGTH_MIN = 1
COMPONENT_OPTION_LENGTH_MAX = 25
COMPONENT_OPTION_MIN_VALUES_MIN = 0
COMPONENT_OPTION_MIN_VALUES_MAX = 15
COMPONENT_OPTION_MAX_VALUES_MIN = 1
COMPONENT_OPTION_MAX_VALUES_MAX = 25


def _debug_component_components(components):
    """
    Checks whether given `component.components` value is correct.
    
    Parameters
    ----------
    components : `None` or (`list`, `tuple`) of ``ComponentBase``
        Sub-components.
    
    Raises
    ------
    AssertionError
        - If `components`'s length is out of the expected range [0:5].
        - If `components` is neither `None`, `tuple` or `list`.
        - If `components` contains a non ``ComponentBase`` instance.
    """
    if (components is None):
        pass
    elif isinstance(components, (tuple, list)):
        if (len(components) > COMPONENT_SUB_COMPONENT_LIMIT):
            raise AssertionError(f'A `component.components` can have maximum 5 sub-components, got '
                f'{len(components)}; {components!r}.')
        
        for component in components:
            if not isinstance(component, ComponentBase):
                raise AssertionError(f'`component` can be given as `{ComponentBase.__name__}` instance, got '
                    f'{component.__class__.__name__}.')
            
            if component.type is COMPONENT_TYPE_ROW:
                raise AssertionError(f'Cannot add `{COMPONENT_TYPE_ROW}` type as sub components, got '
                    f'{component!r}.')
    else:
        raise AssertionError(f'`components` can be given as `None`, `tuple` or `list`, got '
            f'{components.__class__.__name__}.')


def _debug_component_custom_id(custom_id):
    """
    Checks whether given `component.custom_id` value is correct.
    
    Parameters
    ----------
    custom_id : `None` or `str`
        Custom identifier to detect which button was clicked by the user.
    
    Raises
    ------
    AssertionError
        - If `custom_id` was not given neither as `None` or `str` instance.
        - If `custom_id`'s length is over `100`.
    """
    if (custom_id is None):
        pass
    elif isinstance(custom_id, str):
        custom_id_length = len(custom_id)
        if custom_id_length == 0:
            raise AssertionError(f'`custom_id` is not nullable.')
        
        if custom_id_length > COMPONENT_CUSTOM_ID_LENGTH_MAX:
            raise AssertionError(f'`custom_id`\'s max length can be {COMPONENT_CUSTOM_ID_LENGTH_MAX!r}, got '
                f'{len(custom_id)!r}; {custom_id!r}.')
    else:
        raise AssertionError(f'`custom_id` can be given either as `None` or as `str` instance, got '
            f'{custom_id.__class__.__name__}.')


def _debug_component_emoji(emoji):
    """
    Checks whether the given `component.emoji` value is correct.
    
    Parameters
    ----------
    emoji : `None` or ``Emoji``
        Emoji of the button if applicable.
    
    Raises
    ------
    AssertionError
        If `emoji` was not given as ``Emoji`` instance.
    """
    if emoji is None:
        pass
    elif isinstance(emoji, Emoji):
        pass
    else:
        raise AssertionError(f'`emoji` can be given as `{Emoji.__name__}` instance, got '
            f'{emoji.__class__.__name__}')


def _debug_component_label(label):
    """
    Checks whether the given `component.label` value is correct.
    
    Parameters
    ----------
    label : `None` or `str`
        Label of the component.
    
    Raises
    ------
    AssertionError
        - If `label` was not given neither as `None` nor as `int` instance.
        - If `label`'s length is over `80`.
    """
    if label is None:
        pass
    elif isinstance(label, str):
        if len(label) > COMPONENT_LABEL_LENGTH_MAX:
            raise AssertionError(f'`label`\'s max length can be {COMPONENT_LABEL_LENGTH_MAX!r}, got '
                f'{len(label)!r}; {label!r}.')
    else:
        raise AssertionError(f'`label` can be given either as `None` or as `str` instance, got '
            f'{label.__class__.__name__}.')


def _debug_component_enabled(enabled):
    """
    Checks whether the given `component.enabled` value is correct.
    
    Parameters
    ----------
    enabled : `bool`
        Whether the button is enabled.
    
    Raises
    ------
    AssertionError
        If `enabled` was not given as `bool` instance.
    """
    if not isinstance(enabled, bool):
        raise AssertionError(f'`enabled` can be given as `bool` instance, got {enabled.__class__.__name__}.')


def _debug_component_url(url):
    """
    Checks whether the given `component.url` value is correct.
    
    Parameters
    ----------
    url : `None` or `str`
        Url to redirect to when clicking on a button.
    
    Raises
    ------
    AssertionError
        If `url` was not given neither as `None` or `str` instance.
    """
    if url is None:
        pass
    elif isinstance(url, str):
        pass
    else:
        raise AssertionError(f'`url` can be given either as `None` or as `str` instance, got '
            f'{url.__class__.__name__}.')


def _debug_component_value(value):
    """
    Checks whether the given `component_option.value` value is correct.
    
    Parameters
    ----------
    value : `str`
        A component option's value.
    
    Raises
    ------
    AssertionError
        If `value` was not given as `str` instance.
    """
    if not isinstance(value, str):
        raise AssertionError(f'`value` can be given either as  `str` instance, got '
            f'{value.__class__.__name__}.')


def _debug_component_description(description):
    """
    Checks whether the given `component_option.description` value is correct.
    
    Parameters
    ----------
    description : `None` or `str`
        A component option's description.
    
    Raises
    ------
    AssertionError
        If `description` was not given neither as `None` or `str` instance.
    """
    if description is None:
        pass
    elif isinstance(description, str):
        pass
    else:
        raise AssertionError(f'`description` can be given either as `None` or as `str` instance, got '
            f'{description.__class__.__name__}.')


def _debug_component_default(default):
    """
    Checks whether the given `component_option.default` value is correct.
    
    Parameters
    ----------
    default : `bool`
        Whether this component option is the default one.
    
    Raises
    ------
    AssertionError
        If `default` was not given as `bool` instance.
    """
    if not isinstance(default, bool):
        raise AssertionError(f'`default` can be given as `bool` instance, got {default.__class__.__name__}.')


def _debug_component_options(options):
    """
    Checks whether given `component.options` value is correct.
    
    Parameters
    ----------
    options : `None` or (`list`, `tuple`) of ``ComponentSelectOption``
        Sub-options.
    
    Raises
    ------
    AssertionError
        - If `options` is neither `None`, `tuple` or `list`.
        - If `options` contains a non ``ComponentSelectOption`` instance.
        - If `options`'s length is out of the expected [1:25] range.
    """
    if options is None:
        option_length = 0
    if isinstance(options, (tuple, list)):
        for option in options:
            if not isinstance(option, ComponentSelectOption):
                raise AssertionError(f'`option` can be given as `{ComponentSelectOption.__name__}` instance, got '
                    f'{option.__class__.__name__}.')
        
        option_length = len(options)
    else:
        raise AssertionError(f'`options` can be given as `None`, `tuple` or `list`, got '
            f'{options.__class__.__name__}.')
    
    if (option_length < COMPONENT_OPTION_LENGTH_MIN) or (option_length > COMPONENT_OPTION_LENGTH_MAX):
        raise AssertionError(f'`options` can be in range '
            f'[{COMPONENT_OPTION_LENGTH_MIN}:{COMPONENT_OPTION_LENGTH_MAX}], got {option_length}.')


def _debug_component_placeholder(placeholder):
    """
    Checks whether the given `component_option.placeholder` value is correct.
    
    Parameters
    ----------
    placeholder : `None` or `str`
        The placeholder text of a component select.
    
    Raises
    ------
    AssertionError
        - If `placeholder` is neither `None` nor `str` instance.
    """
    if placeholder is None:
        pass
    elif isinstance(placeholder, str):
        pass
    else:
        raise AssertionError(f'`placeholder` can be given as `None or `str` instance, got '
            f'{placeholder.__class__.__name__}.')


def _debug_component_min_values(min_values):
    """
    Checks whether the given `component_option.min_values` value is correct.
    
    Parameters
    ----------
    min_values : `int`
        The min values of a component select.
    
    Raises
    ------
    AssertionError
        - If `min_values` was not given as `int` instance.
        - If `min_values`'s is out of range [0:15].
    """
    if not isinstance(min_values, int):
        raise AssertionError(f'`min_values` can be given as `int` instance, got {min_values.__class__.__name__}.')
    
    if (min_values < COMPONENT_OPTION_MIN_VALUES_MIN) or (min_values > COMPONENT_OPTION_MIN_VALUES_MAX):
        raise AssertionError(f'`min_values` can be in range '
            f'[{COMPONENT_OPTION_MIN_VALUES_MIN}:{COMPONENT_OPTION_MAX_VALUES_MIN}], got {min_values!r}.')


def _debug_component_max_values(max_values):
    """
    Checks whether the given `component_option.max_values` value is correct.
    
    Parameters
    ----------
    max_values : `int`
        The max values of a component select.
    
    Raises
    ------
    AssertionError
        - If `max_values` was not given as `int` instance.
        - If `max_values`'s is out of range [1:25].
    """
    if not isinstance(max_values, int):
        raise AssertionError(f'`max_values` can be given as `int` instance, got {max_values.__class__.__name__}.')

    if (max_values < COMPONENT_OPTION_MAX_VALUES_MIN) or (max_values > COMPONENT_OPTION_MAX_VALUES_MAX):
        raise AssertionError(f'`max_values` can be in range '
            f'[{COMPONENT_OPTION_MAX_VALUES_MIN}:{COMPONENT_OPTION_MAX_VALUES_MAX}], got {max_values!r}.')


def create_auto_custom_id():
    """
    Creates a random custom identifier for components.
    
    Returns
    -------
    custom_id : `str`
        The created custom id.
    """
    return to_base85(random_bytes(64)).decode()


@export
class ComponentBase:
    """
    Base class for 3rd party components.
    
    Class Attributes
    ----------------
    type : ``ComponentType`` = `ComponentType.none`
        The component's type.
    custom_id : `NoneType` = `None`
        Placeholder for sub-classes without `custom_id` attribute.
    """
    __slots__ = ()
    
    type = ComponentType.none
    custom_id = None
    
    @classmethod
    def from_data(cls, data):
        """
        Creates a new message component from the received data.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Message component data.
        
        Returns
        -------
        self : ``ComponentBase`` instance
            The created component instance.
        """
        return None
    
    
    def to_data(self):
        """
        Converts the component to json serializable object.
        
        Returns
        -------
        data : `dict` of (`str`, `Any`) items
        """
        data = {
            'type' : self.type.value
        }
        
        return data
    
    
    def __repr__(self):
        """Returns the message component's representation."""
        return f'<{self.__class__.__name__}>'
    
    
    def copy(self):
        """
        Copies the component.
        
        Returns
        -------
        new : ``ComponentBase``
        """
        return self
    
    
    def copy_with(self, **kwargs):
        """
        Copies the component and modifies the created one with the given parameters.
        
        Parameters
        ----------
        **kwargs : Keyword parameters
            Keyword parameters referencing attributes.
        """
        if kwargs:
            raise TypeError(f'Unused or unsettable attributes: {kwargs}')
        
        return self
    
    
    def __eq__(self, other):
        """Returns Whether the two component are equal."""
        if type(other) is not type(self):
            return NotImplemented
        
        return True
    
    
    def __hash__(self):
        """Returns the component's hash value."""
        return self.type.value
    
    
    def _iter_components(self):
        """
        Iterates over the sub-components recursively of the component including itself.
        
        This method is a generator.
        
        Yields
        ------
        component : ``ComponentBase``
        """
        yield self
        return
    
    
    def _replace_direct_sub_components(self, relation):
        """
        Replaces the sub components of the component with the given relation.
        
        Parameters
        ----------
        relation : `dict` of (``ComponentBase``, ``ComponentBase``) items
            Relation to replace each component with.
        """
        pass
    
    
    def _iter_direct_sub_components(self):
        """
        Iterates over the sub-components of the component.
        
        This method is a generator.
        
        Yields
        ------
        component : ``ComponentBase``
        """
        return
        yield

@export
class ComponentRow(ComponentBase):
    """
    Action row component.
    
    Attributes
    ----------
    components : `None` or `tuple` of ``ComponentBase`` instances
        Stored components.
    
    Class Attributes
    ----------------
    type : ``ComponentType`` = `ComponentType.row`
        The component's type.
    custom_id : `NoneType` = `None`
        `custom_id` is not applicable for component rows.
    """
    type = ComponentType.row
    
    __slots__ = ('components',)
    
    def __new__(cls, *components):
        """
        Creates a new action component from the given components.
        
        Parameters
        ----------
        *components : ``ComponentBase`` instances
            Sub components.
        
        Raises
        ------
        AssertionError
            - If `components` is neither `None`, `tuple` or `list`.
            - If `components` contains a non ``Component`` instance.
        """
        if __debug__:
            _debug_component_components(components)
        
        if not components:
            components = None
        
        self = object.__new__(cls)
        self.components = components
        return self
    
    
    @classmethod
    @copy_docs(ComponentBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        
        component_datas = data.get('components', None)
        if (component_datas is None) or (not component_datas):
            components = None
        else:
            components = [create_component(component_data) for component_data in component_datas]
        self.components = components
        
        return self
    
    
    @copy_docs(ComponentBase.to_data)
    def to_data(self):
        data = {
            'type' : self.type.value
        }
        
        components = self.components
        if (components is None):
            component_datas = []
        else:
            component_datas = [component.to_data() for component in components]
        data['components'] = component_datas
        
        return data
    
    
    @copy_docs(ComponentBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__, ' type=']
        
        type_ = self.type
        repr_parts.append(type_.name)
        repr_parts.append(' (')
        repr_parts.append(repr(type_.value))
        repr_parts.append(')')
        
        repr_parts.append(', components=')
        components = self.components
        if (components is None):
            repr_parts.append('[]')
        else:
            repr_parts.append('[')
            
            index = 0
            limit = len(components)
            
            while True:
                component = components[index]
                index += 1
                
                repr_parts.append(repr(component))
                
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    @copy_docs(ComponentBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        components = self.components
        if (components is not None):
            components = tuple(component.copy() for component in self.components)
        
        new.components = components
        
        return new
    
    
    def copy_with(self, **kwargs):
        """
        Copies the component and modifies the created one with the given parameters.
        
        Parameters
        ----------
        **kwargs : Keyword parameters
            Keyword parameters referencing attributes.
        
        Other Parameters
        ----------------
        components : `iterable` of ``ComponentBase`` instances, Optional (Keyword only)
            Sub components.
        
        Returns
        -------
        new : ``ComponentRow``
        """
        try:
            components = kwargs.pop('components')
        except KeyError:
            components = self.components
        else:
            components = tuple(components)
            
            if __debug__:
                _debug_component_components(components)
            
            if not components:
                components = None
        
        self = object.__new__(type(self))
        self.components = components
        return self
    
    
    @copy_docs(ComponentBase.__eq__)
    def __eq__(self, other):
        if type(other) is not type(self):
            return NotImplemented
        
        if self.components != other.components:
            return False
        
        return True
    
    
    @copy_docs(ComponentBase.__hash__)
    def __hash__(self):
        hash_value = self.type.value
        
        components = self.components
        if (components is not None):
            hash_value ^= len(components)<<12
            for component in components:
                hash_value ^= hash(component)
        
        return hash_value
    
    
    @copy_docs(ComponentBase._iter_components)
    def _iter_components(self):
        yield self
        components = self.components
        if (components is not None):
            for component in components:
                yield from component._iter_components()
    
    
    @copy_docs(ComponentBase._replace_direct_sub_components)
    def _replace_direct_sub_components(self, relation):
        components = self.components
        if (components is not None):
            self.components = tuple(relation.get(component, component) for component in components)
    
    
    @copy_docs(ComponentBase._iter_direct_sub_components)
    def _iter_direct_sub_components(self):
        components = self.components
        if (components is not None):
            yield from components


class ComponentButton(ComponentBase):
    """
    Button component.
    
    Attributes
    ----------
    custom_id : `None` or `str`
        Custom identifier to detect which button was clicked by the user.
        
        > Mutually exclusive with the `url` field.
    enabled : `bool`
        Whether the component is enabled.
    emoji : `None` or ``Emoji``
        Emoji of the button if applicable.
    label : `None` or `str`
        Label of the component.
    style : `None` or ``ButtonStyle``
        The button's style.
    url : `None` or `str`
        Url to redirect to when clicking on the button.
        
        > Mutually exclusive with the `custom_id` field.
    
    Class Attributes
    ----------------
    type : ``ComponentType`` = `ComponentType.button`
        The component's type.
    default_style : ``ButtonStyle`` = `ButtonStyle.violet`
        The default button style to use if style is not given.
    """
    type = ComponentType.button
    default_style = ButtonStyle.violet
    
    __slots__ = ('custom_id', 'enabled', 'emoji', 'label', 'style', 'url',)
    
    def __new__(cls, label=None, emoji=None, *, custom_id=None, url=None, style=None, enabled=True):
        """
        Creates a new component instance with the given parameters.
        
        Parameters
        ----------
        label : `None` or `str`, Optional
            Label of the component.
        emoji : `None` or ``Emoji``, Optional
            Emoji of the button if applicable.
        custom_id : `None` or `str`, Optional (Keyword only)
            Custom identifier to detect which button was clicked by the user.
            
            > Mutually exclusive with the `url` field.
        
        url : `None` or `str`, Optional (Keyword only)
            Url to redirect to when clicking on the button.
            
            > Mutually exclusive with the `custom_id` field.
        
        style : `None`, ``ButtonStyle``, `int`, Optional (Keyword only)
            The button's style.
        
        enabled : `bool`, Optional (Keyword only)
            Whether the button is enabled. Defaults to `True`.
        
        Raises
        ------
        TypeError
            If `style`'s type is unexpected.
        AssertionError
            - If `custom_id` was not given neither as `None` or `str` instance.
            - `url` is mutually exclusive with `custom_id`.
            - If `emoji` was not given as ``Emoji`` instance.
            - If `url` was not given neither as `None` or `str` instance.
            - If `style` was not given as any of the `type`'s expected styles.
            - If `label` was not given neither as `None` nor as `int` instance.
            - If `enabled` was not given as `bool` instance.
            - If `label`'s length is over `80`.
            - If `custom_id`'s length is over `100`.
        """
        if __debug__:
            _debug_component_custom_id(custom_id)
            _debug_component_emoji(emoji)
            _debug_component_label(label)
            _debug_component_enabled(enabled)
            _debug_component_url(url)
        
        if (custom_id is not None) and (not custom_id):
            custom_id = None
        
        if (url is not None) and (not url):
            url = None
        
        if __debug__:
            if (custom_id is not None) and (url is not None):
                raise AssertionError(f'`custom_id` and `url` fields are mutually exclusive, got '
                    f'custom_id={custom_id!r}, url={url!r}.')
        
        if (url is None):
            if style is None:
                style = cls.default_style
            else:
                style = preconvert_preinstanced_type(style, 'style', ButtonStyle)
            
            if (custom_id is None):
                custom_id = create_auto_custom_id()
        
        else:
            style = ButtonStyle.link
        
        if (label is not None) and (not label):
            label = None
        
        self = object.__new__(cls)
        
        self.style = style
        self.custom_id = custom_id
        self.emoji = emoji
        self.url = url
        self.label = label
        self.enabled = enabled
        
        return self
    
    
    @classmethod
    @copy_docs(ComponentBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        
        emoji_data = data.get('emoji', None)
        if emoji_data is None:
            emoji = None
        else:
            emoji = create_partial_emoji_from_data(emoji_data)
        self.emoji = emoji
        
        style = data.get('style', None)
        if (style is not None):
            style = ButtonStyle.get(style)
        self.style = style
        
        self.url = data.get('url', None)
        
        self.custom_id = data.get('custom_id', None)
        
        self.label = data.get('label', None)
        
        self.enabled = not data.get('disabled', False)
        
        return self
    
    
    @copy_docs(ComponentBase.to_data)
    def to_data(self):
        data = {
            'type' : self.type.value
        }
        
        emoji = self.emoji
        if (emoji is not None):
            data['emoji'] = create_partial_emoji_data(emoji)
        
        style = self.style
        if (style is not None):
            data['style'] = style.value
        
        url = self.url
        if (url is not None):
            data['url'] = url
        
        custom_id = self.custom_id
        if (custom_id is not None):
            data['custom_id'] = custom_id
        
        label = self.label
        if (label is not None):
            data['label'] = label
        
        if (not self.enabled):
            data['disabled'] = True
        
        return data
    
    
    @copy_docs(ComponentBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__, ' type=']
        
        type_ = self.type
        repr_parts.append(type_.name)
        repr_parts.append(' (')
        repr_parts.append(repr(type_.value))
        repr_parts.append(')')
        
        style = self.style
        if (style is not None):
            repr_parts.append(', style=')
            repr_parts.append(style.name)
            repr_parts.append(' (')
            repr_parts.append(repr(style.value))
            repr_parts.append(')')
        
        emoji = self.emoji
        if (emoji is not None):
            repr_parts.append(', emoji=')
            repr_parts.append(repr(emoji))
        
        label = self.label
        if (label is not None):
            repr_parts.append(', label=')
            repr_parts.append(reprlib.repr(label))
        
        url = self.url
        if (url is not None):
            repr_parts.append(', url=')
            repr_parts.append(url_cutter(url))
        
        custom_id = self.custom_id
        if (custom_id is not None):
            repr_parts.append(', custom_id=')
            repr_parts.append(reprlib.repr(custom_id))
        
        enabled = self.enabled
        if (not enabled):
            repr_parts.append(', enabled=')
            repr_parts.append(repr(enabled))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    @copy_docs(ComponentBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        new.custom_id = self.custom_id
        new.emoji = self.emoji
        new.style = self.style
        new.url = self.url
        new.label = self.label
        new.enabled = self.enabled
        
        return new
    
    
    def copy_with(self, **kwargs):
        """
        Copies the component and modifies the created one with the given parameters.
        
        Parameters
        ----------
        **kwargs : Keyword parameters
            Keyword parameters referencing attributes.
        
        Other Parameters
        ----------------
        label : `None` or `str`, Optional (Keyword only)
            Label of the component.
        
        emoji : `None` or ``Emoji``, Optional (Keyword only)
            Emoji of the button if applicable.
        
        custom_id : `None` or `str`, Optional (Keyword only)
            Custom identifier to detect which button was clicked by the user.
            
        url : `None` or `str`, Optional (Keyword only)
            Url to redirect to when clicking on the button.
            
        style : `None`, ``ButtonStyle``, `int`, Optional (Keyword only)
            The button's style.
        
        enabled : `bool`, Optional (Keyword only)
            Whether the button is enabled. Defaults to `True`.
        
        Returns
        -------
        new : ``ComponentButton``
        """
        try:
            custom_id = kwargs.pop('custom_id')
        except KeyError:
            custom_id = self.custom_id
        else:
            if __debug__:
                _debug_component_custom_id(custom_id)
        
        try:
            emoji = kwargs.pop('emoji')
        except KeyError:
            emoji = self.emoji
        else:
            if __debug__:
                _debug_component_emoji(emoji)
        
        try:
            label = kwargs.pop('label')
        except KeyError:
            label = self.label
        else:
            if __debug__:
                _debug_component_label(label)
        
        try:
            enabled = kwargs.pop('enabled')
        except KeyError:
            enabled = self.enabled
        else:
            if __debug__:
                _debug_component_enabled(enabled)
        
        try:
            url = kwargs.pop('url')
        except KeyError:
            url = self.url
        else:
            if __debug__:
                _debug_component_url(url)
        
        try:
            style = kwargs.pop('style')
        except KeyError:
            style = self.style
        
        if kwargs:
            raise TypeError(f'Unused or unsettable attributes: {kwargs}')
        
        if (custom_id is not None) and (not custom_id):
            custom_id = None
        
        if (url is not None) and (not url):
            url = None
        
        if __debug__:
            if (custom_id is not None) and (url is not None):
                raise AssertionError(f'`custom_id` and `url` fields are mutually exclusive, got '
                    f'custom_id={custom_id!r}, url={url!r}.')
        
        if (url is None):
            if style is None:
                style = cls.default_style
            else:
                style = preconvert_preinstanced_type(style, 'style', ButtonStyle)
            
            if (custom_id is None):
                custom_id = create_auto_custom_id()
        
        else:
            style = ButtonStyle.link
        
        new = object.__new__(type(self))
        
        new.custom_id = custom_id
        new.emoji = emoji
        new.style = style
        new.url = url
        new.label = label
        new.enabled = enabled
        
        return new
    
    
    @copy_docs(ComponentBase.__eq__)
    def __eq__(self, other):
        if type(other) is not type(self):
            return NotImplemented
        
        if self.emoji is not other.emoji:
            return False
        
        if self.style is not other.style:
            return False
        
        if self.custom_id != other.custom_id:
            return False
        
        if self.url != other.url:
            return False
        
        if self.label != other.label:
            return False
        
        if self.enabled != other.enabled:
            return False
        
        return True
    
    
    @copy_docs(ComponentBase.__hash__)
    def __hash__(self):
        hash_value = self.type.value
        
        emoji = self.emoji
        if (emoji is not None):
            hash_value ^= emoji.id
        
        style = self.style
        if (style is not None):
            hash_value ^= style.value
        
        custom_id = self.custom_id
        if (custom_id is not None):
            hash_value ^= hash(custom_id)
        
        url = self.url
        if (url is not None):
            hash_value ^= hash(url)
        
        label = self.label
        if (label is not None):
            hash_value ^= hash(label)
        
        if self.enabled:
            hash_value ^= 1<<8
        
        return hash_value


class ComponentSelectOption(ComponentBase):
    """
    An option of a select component.
    
    Attributes
    ----------
    default : `bool`
        Whether this option is the default one.
    description : `None` or `str`
        Description of the option.
    emoji : `None` or ``Emoji``
        Emoji on the option if applicable.
    label : `str`
        Label of the option.
    value : `str`
        Identifier value of the option.
    
    Class Attributes
    ----------------
    type : ``ComponentType`` = `ComponentType.none`
        The component's type.
    custom_id : `NoneType` = `None`
        `custom_id` is not applicable for select options.
    """
    __slots__ = ('default', 'description', 'emoji', 'label', 'value')
    
    def __new__(cls, value, label, emoji=None, *, description=None, default=False):
        """
        Creates a new component option with the given parameters.
        
        Parameters
        ----------
        value : `str`
            The option's value.
        label : `str`
            Label of the component option.
        emoji : `None` or ``Emoji``, Optional
            Emoji of the option if applicable.
        description : `None` or `str`, Optional (Keyword only)
            Description of the component option.
        default : `bool`
            Whether this the the default option. Defaults to `False`.
        """
        if __debug__:
            _debug_component_value(value)
            _debug_component_label(label)
            _debug_component_emoji(emoji)
            _debug_component_description(description)
            _debug_component_default(default)
            
            if (label is None) or (not label):
                raise AssertionError('`label` cannot be empty..')
        
        if (description is not None) and (not description):
            description = None
        
        
        self = object.__new__(cls)
        self.default = default
        self.description = description
        self.emoji = emoji
        self.label = label
        self.value = value
        return self
    
    
    @classmethod
    @copy_docs(ComponentBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        
        self.default = data.get('default', False)
        
        self.description = data.get('description', None)
        
        emoji_data = data.get('emoji', None)
        if emoji_data is None:
            emoji = None
        else:
            emoji = create_partial_emoji_from_data(emoji_data)
        self.emoji = emoji
        
        self.label = data['label']
        
        self.value = data['value']
        
        return self
    
    
    @copy_docs(ComponentBase.to_data)
    def to_data(self):
        data = {
            'value': self.value,
            'label': self.label,
        }
        
        emoji = self.emoji
        if (emoji is not None):
            data['emoji'] = create_partial_emoji_data(emoji)
        
        if self.default:
            data['default'] = True
        
        description = self.description
        if (description is not None):
            data['description'] = description
        
        return data


    @copy_docs(ComponentBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__, ' value=', repr(self.value)]
        
        emoji = self.emoji
        if (emoji is not None):
            repr_parts.append(', emoji=')
            repr_parts.append(repr(emoji))
        
        label = self.label
        if (label is not None):
            repr_parts.append(', label=')
            repr_parts.append(reprlib.repr(label))
        
        description = self.description
        if (description is not None):
            repr_parts.append(', description=')
            repr_parts.append(reprlib.repr(description))
        
        if self.default:
            repr_parts.append(', default=')
            repr_parts.append('True')
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
    
    
    @copy_docs(ComponentBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        new.default = self.default
        new.description = self.description
        new.emoji = self.emoji
        new.label = self.label
        new.value = self.value
        return new
    
    
    def copy_with(self, **kwargs):
        """
        Copies the component and modifies the created one with the given parameters.
        
        Parameters
        ----------
        **kwargs : Keyword parameters
            Keyword parameters referencing attributes.
        
        Other Parameters
        ----------------
        value : `str`, Optional (Keyword only)
            The option's value.
        label : `str`, Optional (Keyword only)
            Label of the component option.
        emoji : `None` or ``Emoji``, Optional (Keyword only)
            Emoji of the option if applicable.
        description : `None` or `str`, Optional (Keyword only)
            Description of the component option.
        default : `bool`
            Whether this the the default option. Defaults to `False`.
        
        Returns
        -------
        new : ``ComponentSelectOption``
        """
        try:
            value = kwargs.pop('value')
        except KeyError:
            value = self.value
        else:
            if __debug__:
                _debug_component_value(value)
        
        try:
            label = kwargs.pop('label')
        except KeyError:
            label = self.label
        else:
            if __debug__:
                _debug_component_label(label)
                
                if (label is None) or (not label):
                    raise AssertionError('`label` cannot be empty..')
        
        try:
            emoji = kwargs.pop('emoji')
        except KeyError:
            emoji = self.emoji
        else:
            if __debug__:
                _debug_component_emoji(emoji)
        
        try:
            description = kwargs.pop('description')
        except KeyError:
            description = self.description
        else:
            if __debug__:
                _debug_component_description(description)
            
            if (description is not None) and (not description):
                description = None
        
        try:
            default = kwargs.pop('default')
        except KeyError:
            default = self.default
        else:
            if __debug__:
                _debug_component_default(default)
        
        if kwargs:
            raise TypeError(f'Unused or unsettable attributes: {kwargs}')
        
        new = object.__new__(type(self))
        new.default = default
        new.description = description
        new.emoji = emoji
        new.label = label
        new.value = value
        return new
    
    
    @copy_docs(ComponentBase.__hash__)
    def __hash__(self):
        hash_value = 0
        
        emoji = self.emoji
        if (emoji is not None):
            hash_value ^= emoji.id
        
        value = self.value
        if (value is not None):
            hash_value ^= hash(value)
        
        description = self.description
        if (description is not None):
            hash_value ^= hash(description)
        
        label = self.label
        if (label is not None):
            hash_value ^= hash(label)
        
        if self.default:
            hash_value ^= 1<<8
        
        return hash_value


class ComponentSelect(ComponentBase):
    """
    Select component.
    
    Attributes
    ----------
    custom_id : `str`
        Custom identifier to detect which component was used by the user.
    enabled : `bool`
        Whether the component is enabled.
    options : `None` or `tuple` of ``ComponentSelectOption``
        Options of the select.
    placeholder : `str`
        Placeholder text of the select.
    min_values : `int`
        The minimal amount of options to select. Can be in range [1:15]. Defaults to `1`.
    max_values : `int
        The maximal amount of options to select. Can be in range [1:25]. Defaults to `1`.
    
    Class Attributes
    ----------------
    type : ``ComponentType`` = `ComponentType.select`
        The component's type.
    """
    type = ComponentType.select
    
    __slots__ = ('custom_id', 'enabled', 'options', 'placeholder', 'min_values', 'max_values')
    
    def __new__(cls, options, custom_id=None, *, placeholder=None, min_values=1, max_values=1, enabled=True):
        """
        Creates a new ``ComponentSelect`` instance with the given parameters.
        
        Parameters
        ----------
        options : `None` or (`list`, `tuple`) of ``ComponentSelectOption``
            Options of the select.
        custom_id : `None` or `str`, Optional
            Custom identifier to detect which component was used by the user.
        placeholder : `str`, Optional (Keyword only)
            Placeholder text of the select.
        min_values : `int`, Optional (Keyword only)
            The minimal amount of options to select. Can be in range [1:15]. Defaults to `1`.
        max_values : `int`, Optional (Keyword only)
            The maximal amount of options to select. Can be in range [1:25]. Defaults to `1`.
        enabled : `bool`, Optional (Keyword only)
            Whether the button is enabled. Defaults to `True`.
        
        Raises
        ------
        AssertionError
            - If `custom_id` is not given as `None` or `str` instance.
            - If `custom_id`'s length is out of range [0:100].
            - If `options` length is out from the expected range [1:25].
            - If `options` is neither `None` or (`list`, `tuple`) of ``ComponentSelectOption`` elements.
            - If `min_values` is not `int` instance.
            - If `min_values` is out of range [1:15].
            - If `max_values` is not `int` instance.
            - If `max_values` is out of range [1:25].
            - If `enabled` was not given as `bool` instance.
        """
        if __debug__:
            _debug_component_custom_id(custom_id)
            _debug_component_options(options)
            _debug_component_placeholder(placeholder)
            _debug_component_min_values(min_values)
            _debug_component_max_values(max_values)
            _debug_component_enabled(enabled)
        
        if (placeholder is not None) and (not placeholder):
            placeholder = None
        
        if (custom_id is None) or (not custom_id):
            custom_id = create_auto_custom_id()
        
        if (options is not None):
            options = tuple(options)
            if (not options):
                options = None
        
        self = object.__new__(cls)
        self.custom_id = custom_id
        self.options = options
        self.placeholder = placeholder
        self.min_values = min_values
        self.max_values = max_values
        self.enabled = enabled
        return self
    
    
    @classmethod
    @copy_docs(ComponentBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        
        option_datas = data['options']
        if option_datas:
            options = tuple(ComponentSelectOption.from_data(option_data) for option_data in option_datas)
        else:
            options = None
        self.options = options
        
        self.custom_id = data['custom_id']
        self.placeholder = data.get('placeholder', None)
        self.min_values = data.get('min_values', 1)
        self.max_values = data.get('max_values', 1)
        self.enabled = not data.get('disabled', False)
        
        return self
    
    
    @copy_docs(ComponentBase.to_data)
    def to_data(self):
        data = {
            'type': self.type.value,
            'custom_id': self.custom_id,
        }
        
        options = self.options
        if options is None:
            options_value = []
        else:
            options_value = [option.to_data() for option in options]
        data['options'] = options_value
        
        placeholder = self.placeholder
        if (placeholder is not None):
            data['placeholder'] = placeholder
        
        min_values = self.min_values
        if min_values != 1:
            data['min_values'] = min_values
        
        max_values = self.max_values
        if max_values != 1:
            data['max_values'] = max_values
        
        if (not self.enabled):
            data['disabled'] = True
        
        return data
    
    
    @copy_docs(ComponentBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__, ' type=']
        
        type_ = self.type
        repr_parts.append(type_.name)
        repr_parts.append(' (')
        repr_parts.append(repr(type_.value))
        repr_parts.append(')')
        
        repr_parts.append(', custom_id=')
        repr_parts.append(reprlib.repr(self.custom_id))
        
        repr_parts.append(', options=')
        options = self.options
        if (options is None):
            repr_parts.append('[]')
        else:
            repr_parts.append('[')
            
            index = 0
            limit = len(options)
            
            while True:
                option = options[index]
                index += 1
                
                repr_parts.append(repr(option))
                
                if index == limit:
                    break
                
                repr_parts.append(', ')
                continue
            
            repr_parts.append(']')
        
        repr_parts.append('>')
        
        placeholder = self.placeholder
        if (placeholder is not None):
            repr_parts.append(', placeholder=')
            repr_parts.append(repr(placeholder))
        
        min_values = self.min_values
        if min_values != 1:
            repr_parts.append(', min_values=')
            repr_parts.append(repr(min_values))
        
        max_values = self.max_values
        if max_values != 1:
            repr_parts.append(', max_values=')
            repr_parts.append(repr(max_values))
        
        enabled = self.enabled
        if (not enabled):
            repr_parts.append(', enabled=')
            repr_parts.append(repr(enabled))
        
        return ''.join(repr_parts)
    
    
    @copy_docs(ComponentBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        new.custom_id = self.custom_id
        
        options = self.options
        if (options is not None):
            options = tuple(option.copy() for option in options)
        
        new.options = options
        
        new.placeholder = self.placeholder
        new.min_values = self.min_values
        new.max_values = self.max_values
        new.enabled = self.enabled
        
        return new
    
    
    def copy_with(self, **kwargs):
        """
        Copies the component and modifies the created one with the given parameters.
        
        Parameters
        ----------
        **kwargs : Keyword parameters
            Keyword parameters referencing attributes.
        
        Other Parameters
        ----------------
        options : `None` or (`list`, `tuple`) of ``ComponentSelectOption``, Optional (Keyword only)
            Options of the select.
        custom_id : `None` or `str`, Optional (Keyword only)
            Custom identifier to detect which component was used by the user.
        placeholder : `str`, Optional (Keyword only)
            Placeholder text of the select.
        min_values : `int`, Optional (Keyword only)
            The minimal amount of options to select. Can be in range [1:15]. Defaults to `1`.
        max_values : `int`, Optional (Keyword only)
            The maximal amount of options to select. Can be in range [1:25]. Defaults to `1`.
        
        enabled : `bool`, Optional (Keyword only)
            Whether the button is enabled. Defaults to `True`.
        
        Returns
        -------
        new : ``ComponentSelect``
        """
        try:
            options = kwargs.pop('options')
        except KeyError:
            options = self.options
            if (options is not None):
                options = tuple(option.copy() for option in options)
        else:
            if __debug__:
                _debug_component_options(options)
            
            if (options is not None):
                options = tuple(options)
                if (not options):
                    options = None
        
        try:
            custom_id = kwargs.pop('custom_id')
        except KeyError:
            custom_id = self.custom_id
        else:
            if __debug__:
                _debug_component_custom_id(custom_id)
            
            if custom_id is None:
                custom_id = self.custom_id
        
        try:
            placeholder = kwargs.pop('placeholder')
        except KeyError:
            placeholder = self.placeholder
        else:
            if __debug__:
                _debug_component_placeholder(placeholder)
            
            if (placeholder is not None) and (not placeholder):
                placeholder = None
        
        try:
            min_values = kwargs.pop('min_values')
        except KeyError:
            min_values = self.min_values
        else:
            if __debug__:
                _debug_component_min_values(min_values)
        
        try:
            max_values = kwargs.pop('max_values')
        except KeyError:
            max_values = self.max_values
        else:
            if __debug__:
                _debug_component_max_values(max_values)
        
        try:
            enabled = kwargs.pop('enabled')
        except KeyError:
            enabled = self.enabled
        else:
            if __debug__:
                _debug_component_enabled(enabled)
        
        if kwargs:
            raise TypeError(f'Unused or unsettable attributes: {kwargs}')
        
        new = object.__new__(type(self))
        new.custom_id = custom_id
        new.options = options
        new.placeholder = placeholder
        new.min_values = min_values
        new.max_values = max_values
        new.enabled = enabled
        return new
    
    
    @copy_docs(ComponentBase.__eq__)
    def __eq__(self, other):
        if type(other) is not type(self):
            return NotImplemented
        
        if self.custom_id != other.custom_id:
            return False
        
        if self.options != other.options:
            return False
        
        if self.placeholder != other.placeholder:
            return False
        
        if self.min_values != other.min_values:
            return False
        
        if self.max_values != other.max_values:
            return False
        
        if self.enabled != other.enabled:
            return False
        
        return True
    
    
    @copy_docs(ComponentBase.__hash__)
    def __hash__(self):
        hash_value = self.type.value ^hash(self.custom_id)
        
        options = self.options
        if (options is not None):
            hash_value ^= len(options)<<12
            for option in options:
                hash_value ^= hash(option)
        
        placeholder = self.placeholder
        if (placeholder is not None):
            hash_value ^= hash(placeholder)
        
        hash_value ^= self.min_values
        hash_value ^= self.max_values
        
        if self.enabled:
            hash_value ^= 1<<8
        
        return hash_value
    
    
    @copy_docs(ComponentBase._iter_components)
    def _iter_components(self):
        yield self
        options = self.options
        if (options is not None):
            for option in options:
                yield from option._iter_components()
    
    
    @copy_docs(ComponentBase._replace_direct_sub_components)
    def _replace_direct_sub_components(self, relation):
        options = self.options
        if (options is not None):
            self.options = tuple(relation.get(option, option) for option in options)
    
    
    @copy_docs(ComponentBase._iter_direct_sub_components)
    def _iter_direct_sub_components(self):
        options = self.options
        if (options is not None):
            yield from options


def dynamic_component_style_serializer(style):
    if isinstance(style, PreinstancedBase):
        style = style.value
    
    return style


COMPONENT_DYNAMIC_SERIALIZERS = {
    'emoji': create_partial_emoji_data,
    'style': dynamic_component_style_serializer,
}

del dynamic_component_style_serializer

COMPONENT_DYNAMIC_DESERIALIZERS = {
    'emoji': create_partial_emoji_from_data,
}


COMPONENT_ATTRIBUTE_NAMES = frozenset((
    'components',
    'custom_id',
    'disabled',
    'emoji',
    'label',
    'style',
    'url',
    'options',
    'placeholder',
    'min_values',
    'max_values',
))


class ComponentDynamic(ComponentBase):
    """
    Dynamic component type for not implemented component models.
    
    Attributes
    ----------
    _data : `dict` of (`str`, `Any`)
        The dynamically stored attributes of the component.
    type : ``ComponentType``
        The component's type.
    """
    __slots__ = ('_data', 'type')
    def __new__(cls, type_, **kwargs):
        """
        Creates a new component instance.
        
        Parameters
        ----------
        type_ : ``ComponentType``, `int`
            The component's type.
        **kwargs : Keyword parameters
            Additional attributes of the component.
        """
        type_ = preconvert_preinstanced_type(type_, 'type_', ComponentType)
        
        self = object.__new__(cls)
        self.type = type_
        self._data = kwargs
        return self
    
    
    @classmethod
    @copy_docs(ComponentBase.from_data)
    def from_data(cls, data):
        self = object.__new__(cls)
        self.type = ComponentType.get(data['type'])
        
        validated_data = {}
        for key, value in data.items():
            if key == 'type':
                continue
            
            try:
                deserializer = COMPONENT_DYNAMIC_DESERIALIZERS[key]
            except KeyError:
                pass
            else:
                value = deserializer(value)
            
            validated_data[key] = value
        
        self._data = validated_data
        
        return self
    
    
    @copy_docs(ComponentBase.to_data)
    def to_data(self):
        data = {
            'type' : self.type.value
        }
        
        for key, value in self._data:
            try:
                serializer = COMPONENT_DYNAMIC_DESERIALIZERS[key]
            except KeyError:
                pass
            else:
                value = serializer(value)
            
            data[key] = value
        
        return data
    
    
    @copy_docs(ComponentBase.__repr__)
    def __repr__(self):
        repr_parts = ['<', self.__class__.__name__, ' type=']
        
        type_ = self.type
        repr_parts.append(type_.name)
        repr_parts.append(' (')
        repr_parts.append(repr(type_.value))
        repr_parts.append(')')
        
        for key, value in self._data:
            if value is None:
                continue
            
            if isinstance(value, str):
                value = reprlib.repr(value)
            else:
                value = repr(value)
            
            repr_parts.append(', ')
            repr_parts.append(key)
            repr_parts.append('=')
            repr_parts.append(value)
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    @copy_docs(ComponentBase.copy)
    def copy(self):
        new = object.__new__(type(self))
        
        new.type = self.type
        new._data = self._data.copy()
        
        return new
    
    
    def copy_with(self, **kwargs):
        """
        Copies the component and modifies the created one with the given parameters.
        
        > Dynamic component do not accepts any additional attributes, and returns just a copy of itself.
        
        Parameters
        ----------
        **kwargs : Keyword parameters
            Keyword parameters referencing attributes.
        
        Returns
        -------
        new : ``ComponentDynamic``
        """
        if kwargs:
            raise TypeError(f'Unused or unsettable attributes: `{kwargs}`')
        
        return self.copy()
    
    
    @copy_docs(ComponentBase.__eq__)
    def __eq__(self, other):
        if type(other) is not type(self):
            return NotImplemented
        
        if self.type is not other.type:
            return False
        
        if self._data != other._data:
            return False
        
        return True
    
    
    @copy_docs(ComponentBase.__hash__)
    def __hash__(self):
        return object.__hash__(self)
    
    
    def __getattr__(self, attribute_name):
        """Returns the component's fields if applicable"""
        try:
            attribute_value = self._data[attribute_name]
        except KeyError:
            if attribute_name in COMPONENT_ATTRIBUTE_NAMES:
                attribute_value = None
            else:
                raise AttributeError(attribute_name)
        
        return attribute_value


COMPONENT_TYPE_TO_STYLE = {
    ComponentType.row: None,
    ComponentType.button: ButtonStyle,
    ComponentType.select: None,
}

COMPONENT_TYPE_VALUE_TO_TYPE = {
    ComponentType.row.value: ComponentRow,
    ComponentType.button.value: ComponentButton,
    ComponentType.select.value: ComponentSelect,
}

@export
def create_component(component_data):
    """
    Creates a component from the given component data.
    
    Parameters
    ----------
    component_data : `dict` of (`str`, `Any`)
        Component data.
    
    Returns
    -------
    component : ``ComponentBase``
        the created component instance.
    """
    return COMPONENT_TYPE_VALUE_TO_TYPE.get(component_data['type'], ComponentDynamic).from_data(component_data)
