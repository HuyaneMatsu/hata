import vampytest

from .. import ApplicationCommandOption, ApplicationCommandOptionType
from ..constants import APPLICATION_COMMAND_OPTION_MIN_LENGTH_MAX


def test__ApplicationCommandOption__constructor__from_data__0():
    """
    Tests whether ``ApplicationCommandOption``'s `from_data` method works correctly.
    
    Case: Optional fields are missing.
    """
    name = 'owo'
    description = 'not owo'
    type_ = ApplicationCommandOptionType.string
    
    data = {
        'name': name,
        'description': description,
        'type': type_.value,
    }
    
    option = ApplicationCommandOption.from_data(data)
    
    vampytest.assert_eq(option.name, name)
    vampytest.assert_eq(option.description, description)
    vampytest.assert_is(option.type, type_)
    
    vampytest.assert_eq(option.min_length, 0)
    vampytest.assert_eq(option.max_length, 0)


def test__ApplicationCommandOption__constructor__from_data__1():
    """
    Tests whether ``ApplicationCommandOption``'s `from_data` method works correctly.
    
    Case: Optional fields are set.
    """
    name = 'owo'
    description = 'not owo'
    type_ = ApplicationCommandOptionType.string
    max_length = 30
    min_length = 10
    
    data = {
        'name': name,
        'description': description,
        'type': type_.value,
        'min_length': min_length,
        'max_length': max_length,
    }
    
    option = ApplicationCommandOption.from_data(data)
    
    vampytest.assert_eq(option.name, name)
    vampytest.assert_eq(option.description, description)
    vampytest.assert_is(option.type, type_)
    vampytest.assert_eq(option.min_length, min_length)
    vampytest.assert_eq(option.max_length, max_length)


def test__ApplicationCommandOption__constructor__from_data__2():
    """
    Tests whether ``ApplicationCommandOption.from_data` works as intended.
   
    Case: whether max length defaults back to `0` when given as limit.
    """
    name = 'owo'
    description = 'not owo'
    type_ = ApplicationCommandOptionType.string
    max_length = APPLICATION_COMMAND_OPTION_MIN_LENGTH_MAX
    
    data = {
        'name': name,
        'description': description,
        'type': type_.value,
        'max_length': max_length,
    }
    
    option = ApplicationCommandOption.from_data(data)
    
    vampytest.assert_eq(option.max_length, 0)



def test__ApplicationCommandOption__constructor__to_data__0():
    """
    Tests whether ``ApplicationCommandOption``'s `to_data` method works correctly.
    
    Case: Check whether default fields are present.
    """
    name = 'owo'
    description = 'not owo'
    type_ = ApplicationCommandOptionType.integer
    
    option = ApplicationCommandOption(name, description, type_)
    
    data = option.to_data()
    
    vampytest.assert_in('name', data)
    vampytest.assert_in('description', data)
    vampytest.assert_in('type', data)
    
    vampytest.assert_eq(data['name'], name)
    vampytest.assert_eq(data['description'], description)
    vampytest.assert_eq(data['type'], type_.value)


def test__ApplicationCommandOption__constructor__to_data__1():
    """
    Tests whether ``ApplicationCommandOption``'s `to_data` method works correctly.
    
    Case: String values are not present when option type is not string.
    """
    option = ApplicationCommandOption(
        'owo',
        'owo',
        ApplicationCommandOptionType.integer
    )
    
    data = option.to_data()
    
    vampytest.assert_not_in('min_length', data)
    vampytest.assert_not_in('max_length', data)


def test__ApplicationCommandOption__constructor__to_data__2():
    """
    Tests whether ``ApplicationCommandOption``'s `to_data` method works correctly.
   
    Case: string values are present when option type is indeed string.
    """
    max_length = 30
    min_length = 10
    
    option = ApplicationCommandOption(
        'owo',
        'owo',
        ApplicationCommandOptionType.string,
        min_length = min_length,
        max_length = max_length,
    )
    
    data = option.to_data()
    
    vampytest.assert_in('min_length', data)
    vampytest.assert_in('max_length', data)

    vampytest.assert_eq(data['min_length'], min_length)
    vampytest.assert_eq(data['max_length'], max_length)
