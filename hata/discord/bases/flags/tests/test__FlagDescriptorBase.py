import vampytest

from ..flag_descriptors import FlagDescriptorBase, NAME_UNKNOWN


def _assert_fields_set(flag_descriptor):
    """
    Asserts whether the given flag descriptor has all of its fields set.
    
    Parameters
    ----------
    flag_descriptor : ``FlagDescriptorBase``
        The flag descriptor to check.
    """
    vampytest.assert_instance(flag_descriptor, FlagDescriptorBase)


class InstantiableFlagDescriptorBase(FlagDescriptorBase):
    def __new__(cls):
        return object.__new__(cls)


def test__flag_descriptors__new():
    """
    Tests whether ``FlagDescriptorBase.__new__`` works as intended.
    """
    with vampytest.assert_raises(NotImplementedError):
        FlagDescriptorBase()


def test__build_cannot_exception():
    """
    Tests whether ``FlagDescriptorBase._build_cannot_exception`` works as intended.
    """
    flag_descriptor = InstantiableFlagDescriptorBase()
    action = 'eat'
    output = flag_descriptor._build_cannot_exception(action)
    vampytest.assert_instance(output, AttributeError)
    exception_parameters = output.args
    vampytest.assert_eq(len(exception_parameters), 1)
    message = exception_parameters[0]
    vampytest.assert_instance(message, str)
    vampytest.assert_eq(message, f'Cannot {action} `{NAME_UNKNOWN}.{NAME_UNKNOWN}`.')


def test__FlagDescriptorBase__get__type():
    """
    Tests whether ``FlagDescriptorBase.__get__`` works as intended.
    
    Case: from type.
    """
    instance = None
    instance_type = int
    
    flag_descriptor = InstantiableFlagDescriptorBase()
    output = type(flag_descriptor).__get__(flag_descriptor, instance, instance_type)
    
    vampytest.assert_instance(output, FlagDescriptorBase)
    vampytest.assert_is(output, flag_descriptor)


def test__FlagDescriptorBase__get__instance():
    """
    Tests whether ``FlagDescriptorBase.__get__`` works as intended.
    
    Case: from instance.
    """
    instance = 3
    instance_type = int
    
    flag_descriptor = InstantiableFlagDescriptorBase()
    output = type(flag_descriptor).__get__(flag_descriptor, instance, instance_type)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__FlagDescriptorBase__set():
    """
    Tests whether ``FlagDescriptorBase.__set__`` works as intended.
    """
    instance = 3
    
    flag_descriptor = InstantiableFlagDescriptorBase()
    
    with vampytest.assert_raises(AttributeError):
        type(flag_descriptor).__set__(flag_descriptor, instance, 3)


def test__FlagDescriptorBase__delete():
    """
    Tests whether ``FlagDescriptorBase.__delete__`` works as intended.
    """
    instance = 3
    
    flag_descriptor = InstantiableFlagDescriptorBase()
    
    with vampytest.assert_raises(AttributeError):
        type(flag_descriptor).__delete__(flag_descriptor, instance)


def test__FlagDescriptorBase__repr():
    """
    Tests whether ``FlagDescriptorBase.__repr__`` works as intended.
    """
    flag_descriptor = InstantiableFlagDescriptorBase()
    
    output = repr(flag_descriptor)
    vampytest.assert_instance(output, str)
    vampytest.assert_in(type(flag_descriptor).__name__, output)
    vampytest.assert_in(f'name = {flag_descriptor.name!r}', output)
    vampytest.assert_in(f'shift = {0!r}', output)


def _iter_options__eq():
    keyword_parameters = {}
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__FlagDescriptorBase__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``FlagDescriptorBase.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    flag_descriptor_0 = InstantiableFlagDescriptorBase(**keyword_parameters_0)
    flag_descriptor_1 = InstantiableFlagDescriptorBase(**keyword_parameters_1)
    
    output = flag_descriptor_0 == flag_descriptor_1
    vampytest.assert_instance(output, bool)
    return output


def test__FlagDescriptorBase__hash():
    """
    Tests whether ``FlagDescriptorBase.__hash__`` works as intended.
    """
    flag_descriptor = InstantiableFlagDescriptorBase()
    
    output = hash(flag_descriptor)
    vampytest.assert_instance(output, int)


def _iter_options__properties():
    keyword_parameters = {}
    
    yield (
        keyword_parameters,
        InstantiableFlagDescriptorBase.flag_name,
        'flag_name',
        NAME_UNKNOWN,
    )
    
    yield (
        keyword_parameters,
        InstantiableFlagDescriptorBase.type_name,
        'type_name',
        NAME_UNKNOWN,
    )
    
    yield (
        keyword_parameters,
        InstantiableFlagDescriptorBase.mask,
        'mask',
        0,
    )
    
    yield (
        keyword_parameters,
        InstantiableFlagDescriptorBase.shift,
        'shift',
        0,
    )
    
    yield (
        keyword_parameters,
        InstantiableFlagDescriptorBase.name,
        'name',
        f'{NAME_UNKNOWN}.{NAME_UNKNOWN}',
    )
    
    yield (
        keyword_parameters,
        InstantiableFlagDescriptorBase.deprecation,
        'deprecation',
        None,
    )


@vampytest._(vampytest.call_from(_iter_options__properties()).returning_last())
def test__FlagDescriptorBase__properties(keyword_parameters, property, case_name):
    """
    Check whether ``FlagDescriptorBase`` properties work.
    
    Parameters
    ----------
    keyword_parameters : `dict<str, object>`
        Keyword parameters to create instance with.
    
    property : ``Property``
        Property to use.
    
    case_name : `str`
        The cases name. Here because python cant write `__repr__` lmeow.
    
    Returns
    -------
    output : `object`
    """
    flag_descriptor = InstantiableFlagDescriptorBase(**keyword_parameters)
    return property.fget(flag_descriptor)
