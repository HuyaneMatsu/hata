import vampytest

from ..standard import PlaceHolder


def _assert_fields_set(place_holder):
    """
    Asserts whether every fields are set of the given place holder.
    
    Parameters
    ----------
    place_holder : ``PlaceHolder``
        The place holder to check.
    """
    vampytest.assert_instance(place_holder, PlaceHolder)
    vampytest.assert_instance(place_holder.attribute_name, str, nullable = True)
    vampytest.assert_instance(place_holder.default_value, object)
    vampytest.assert_instance(place_holder.docs, str, nullable = True)
    vampytest.assert_instance(place_holder.type_name, str, nullable = True)


def test__PlaceHolder__new__min_fields():
    """
    Tests whether ``PlaceHolder.__new__`` works as intended.
    
    Case: Minimal amount of fields given.
    """
    default_value = 4
    
    place_holder = PlaceHolder(default_value)
    
    _assert_fields_set(place_holder)
    
    vampytest.assert_eq(place_holder.default_value, default_value)


def test__PlaceHolder__new__max_fields():
    """
    Tests whether ``PlaceHolder.__new__`` works as intended.
    
    Case: Maximal amount of fields given.
    """
    default_value = 4
    docs = 'hey mister'
    
    place_holder = PlaceHolder(default_value, docs)
    _assert_fields_set(place_holder)
    
    vampytest.assert_eq(place_holder.default_value, default_value)
    vampytest.assert_eq(place_holder.docs, docs)


def _iter_options__eq():
    default_value = 4
    docs = 'hey mister'
    owner = int
    attribute_name = 'remilia'
    
    keyword_parameters = {
        'default_value': default_value,
        'docs': docs,
    }
    
    set_name_parameters = {
        'owner': owner,
        'attribute_name': attribute_name,
    }
    
    
    yield (
        keyword_parameters,
        set_name_parameters,
        
        keyword_parameters,
        set_name_parameters,
        
        True,
    )
    
    yield (
        keyword_parameters,
        set_name_parameters, 
        {
            **keyword_parameters,
            'default_value': 5,
        },
        set_name_parameters,
        
        False,
    )
    
    yield (
        keyword_parameters,
        set_name_parameters, 
        {
            **keyword_parameters,
            'docs': 'nyan',
        },
        set_name_parameters,
        
        False,
    )
    
    yield (
        keyword_parameters,
        set_name_parameters,
        
        keyword_parameters,
        {
            **set_name_parameters,
            'owner': str,
        },
        
        False,
    )
    
    yield (
        keyword_parameters,
        set_name_parameters,
        
        keyword_parameters,
        {
            **set_name_parameters,
            'attribute_name': 'flandre',
        },
        
        False,
    )
    

@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__PlaceHolder__eq(keyword_parameters_0, set_name_parameters_0, keyword_parameters_1, set_name_parameters_1):
    """
    Tests whether ``PlaceHolder.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    set_name_parameters_0 : `dict<str, object>`
        Keyword parameters to call set name on the instance.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    set_name_parameters_1 : `dict<str, object>`
        Keyword parameters to call set name on the instance.
    
    Returns
    -------
    output : `bool`
    """
    place_holder_0 = PlaceHolder(**keyword_parameters_0)
    place_holder_0.__set_name__(**set_name_parameters_0)
    place_holder_1 = PlaceHolder(**keyword_parameters_1)
    place_holder_1.__set_name__(**set_name_parameters_1)
    
    output = place_holder_0 == place_holder_1
    vampytest.assert_instance(output, bool)
    return output


def test__PlaceHolder__repr__min_fields():
    """
    Tests whether ``PlaceHolder.__repr__`` works as intended.
    
    Case: Minimal amount of fields given.
    """
    default_value = 4
    place_holder = PlaceHolder(default_value)
    
    output = repr(place_holder)
    vampytest.assert_instance(output, str)
    vampytest.assert_in(type(place_holder).__name__, output)
    vampytest.assert_in(f'default_value = {default_value!r}', output)


def test__PlaceHolder__repr__max_fields():
    """
    Tests whether ``PlaceHolder.__repr__`` works as intended.
    
    Case: Maximal amount of fields given.
    """
    default_value = 4
    docs = 'hey mister'
    owner = int
    attribute_name = 'remilia'
    type_name = owner.__name__
    
    place_holder = PlaceHolder(default_value, docs)
    place_holder.__set_name__(owner, attribute_name)
    
    output = repr(place_holder)
    vampytest.assert_instance(output, str)
    vampytest.assert_in(type(place_holder).__name__, output)
    vampytest.assert_in(f'of {type_name}.{attribute_name}', output)
    vampytest.assert_in(f'docs = {docs!r}', output)
    vampytest.assert_in(f'default_value = {default_value!r}', output)


def test__PlaceHolder__hash():
    """
    Tests whether ``PlaceHolder.__hash__`` works as intended.
    """
    default_value = 4
    docs = 'hey mister'
    owner = int
    attribute_name = 'remilia'
    
    place_holder = PlaceHolder(default_value, docs)
    place_holder.__set_name__(owner, attribute_name)
    
    output = hash(place_holder)
    vampytest.assert_instance(output, int)


def test__PlaceHolder__set_name():
    """
    Tests whether ``PlaceHolder.__set_name__`` works as intended.
    """
    default_value = 4
    owner = int
    attribute_name = 'remilia'
    type_name = owner.__name__
    
    place_holder = PlaceHolder(default_value)
    
    place_holder.__set_name__(owner, attribute_name)
    
    _assert_fields_set(place_holder)
    vampytest.assert_eq(place_holder.attribute_name, attribute_name)
    vampytest.assert_eq(place_holder.type_name, type_name)


def test__PlaceHolder__get__from_instance():
    """
    Tests whether ``PlaceHolder.__get__`` works as intended.
    
    Case: from instance.
    """
    default_value = 4
    
    instance = 2
    instance_type = int
    
    place_holder = PlaceHolder(default_value)
    
    output = place_holder.__get__(instance, instance_type)
    vampytest.assert_instance(output, type(default_value))
    vampytest.assert_eq(output, default_value)


def test__PlaceHolder__get__from_type():
    """
    Tests whether ``PlaceHolder.__get__`` works as intended.
    
    Case: from instance.
    """
    default_value = 4
    
    instance = None
    instance_type = int
    
    place_holder = PlaceHolder(default_value)
    
    output = place_holder.__get__(instance, instance_type)
    vampytest.assert_instance(output, type(place_holder))
    vampytest.assert_is(output, place_holder)


def test__PlaceHolder__set():
    """
    Tests whether ``PlaceHolder.__set__`` works as intended.
    
    Case: from instance.
    """
    default_value = 4
    
    instance = 2
    value = 4
    
    place_holder = PlaceHolder(default_value)
    
    with vampytest.assert_raises(NotImplementedError):
        place_holder.__set__(instance, value)


def test__PlaceHolder__del():
    """
    Tests whether ``PlaceHolder.__del__`` works as intended.
    
    Case: from instance.
    """
    default_value = 4
    
    instance = 2
    
    place_holder = PlaceHolder(default_value)
    
    with vampytest.assert_raises(NotImplementedError):
        place_holder.__delete__(instance)
