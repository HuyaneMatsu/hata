import vampytest

from .. import ApplicationCommandOption, ApplicationCommandOptionType

def test__ApplicationCommandOption__constructor__from_data_0():
    """
    Tests whether ``ApplicationCommandOption``'s `from_data` method works correctly.
    This test tests the case when the values are missing.
    """
    data = {
        'description': 'owo',
        'name': 'owo',
        'type': ApplicationCommandOptionType.string.value,
    }
    
    option = ApplicationCommandOption.from_data(data)
    
    vampytest.assert_eq(option.min_length, 0)
    vampytest.assert_eq(option.max_length, 0)


def test__ApplicationCommandOption__constructor__from_data_1():
    """
    Tests whether ``ApplicationCommandOption``'s `from_data` method works correctly.
    This test tests the case when the values are the default ones.
    """
    data = {
        'description': 'owo',
        'name': 'owo',
        'type': ApplicationCommandOptionType.string.value,
        'min_length': 0,
        'max_length': 0,
    }
    
    option = ApplicationCommandOption.from_data(data)
    
    vampytest.assert_eq(option.min_length, 0)
    vampytest.assert_eq(option.max_length, 0)


def test__ApplicationCommandOption__constructor__from_data_2():
    """
    Tests whether ``ApplicationCommandOption``'s `from_data` method works correctly.
    This test tests the case when the values are actually set.
    """
    data = {
        'description': 'owo',
        'name': 'owo',
        'type': ApplicationCommandOptionType.string.value,
        'min_length': 30,
        'max_length': 50,
    }
    
    option = ApplicationCommandOption.from_data(data)
    
    vampytest.assert_eq(option.min_length, 30)
    vampytest.assert_eq(option.max_length, 50)


def test__ApplicationCommandOption__constructor__to_data_0():
    """
    Tests whether ``ApplicationCommandOption``'s `to_data` method works correctly.
    This test tests whether string values are not present when option type is not string.
    """
    option = ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.integer)
    
    data = option.to_data()
    
    vampytest.assert_not_in('min_length', data)
    vampytest.assert_not_in('max_length', data)


def test__ApplicationCommandOption__constructor__to_data_1():
    """
    Tests whether ``ApplicationCommandOption``'s `to_data` method works correctly.
    This test tests whether string values are present when option type is indeed string.
    """
    option = ApplicationCommandOption('owo', 'owo', ApplicationCommandOptionType.string, min_length=30, max_length=50)
    
    data = option.to_data()
    
    vampytest.assert_in('min_length', data)
    vampytest.assert_in('max_length', data)

    vampytest.assert_eq(data['min_length'], 30)
    vampytest.assert_eq(data['max_length'], 50)
