import vampytest

from ..radio_group_option import RadioGroupOption


def _assert_fields_set(radio_group_option):
    """
    Checks whether all attributes of the radio group option are set.
    
    Parameters
    ----------
    radio_group_option : ``RadioGroupOption``
        The radio group option to check.
    """
    vampytest.assert_instance(radio_group_option, RadioGroupOption)
    
    vampytest.assert_instance(radio_group_option.default, bool)
    vampytest.assert_instance(radio_group_option.description, str, nullable = True)
    vampytest.assert_instance(radio_group_option.label, str)
    vampytest.assert_instance(radio_group_option.value, str)


def test__RadioGroupOption__new__no_fields():
    """
    Tests whether ``RadioGroupOption`` works as intended.
    
    Case: no fields given.
    """
    value = 'last'
    
    radio_group_option = RadioGroupOption(value)
    _assert_fields_set(radio_group_option)
    
    vampytest.assert_eq(radio_group_option.value, value)
    vampytest.assert_eq(radio_group_option.label, value)


def test__RadioGroupOption__new__all_fields():
    """
    Tests whether ``RadioGroupOption.__new__`` works as intended.
    
    Case: all fields given.
    """
    value = 'last'
    label = 'night'
    default = True
    description = 'good'
    
    radio_group_option = RadioGroupOption(value, label, default = default, description = description)
    _assert_fields_set(radio_group_option)
    
    vampytest.assert_eq(radio_group_option.value, value)
    vampytest.assert_eq(radio_group_option.label, label)
    vampytest.assert_eq(radio_group_option.default, default)
    vampytest.assert_eq(radio_group_option.description, description)
