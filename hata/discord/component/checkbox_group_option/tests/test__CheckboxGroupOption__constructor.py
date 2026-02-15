import vampytest

from ..checkbox_group_option import CheckboxGroupOption


def _assert_fields_set(checkbox_group_option):
    """
    Checks whether all attributes of the checkbox group option are set.
    
    Parameters
    ----------
    checkbox_group_option : ``CheckboxGroupOption``
        The checkbox group option to check.
    """
    vampytest.assert_instance(checkbox_group_option, CheckboxGroupOption)
    
    vampytest.assert_instance(checkbox_group_option.default, bool)
    vampytest.assert_instance(checkbox_group_option.description, str, nullable = True)
    vampytest.assert_instance(checkbox_group_option.label, str)
    vampytest.assert_instance(checkbox_group_option.value, str)


def test__CheckboxGroupOption__new__no_fields():
    """
    Tests whether ``CheckboxGroupOption`` works as intended.
    
    Case: no fields given.
    """
    value = 'last'
    
    checkbox_group_option = CheckboxGroupOption(value)
    _assert_fields_set(checkbox_group_option)
    
    vampytest.assert_eq(checkbox_group_option.value, value)
    vampytest.assert_eq(checkbox_group_option.label, value)


def test__CheckboxGroupOption__new__all_fields():
    """
    Tests whether ``CheckboxGroupOption.__new__`` works as intended.
    
    Case: all fields given.
    """
    value = 'last'
    label = 'night'
    default = True
    description = 'good'
    
    checkbox_group_option = CheckboxGroupOption(value, label, default = default, description = description)
    _assert_fields_set(checkbox_group_option)
    
    vampytest.assert_eq(checkbox_group_option.value, value)
    vampytest.assert_eq(checkbox_group_option.label, label)
    vampytest.assert_eq(checkbox_group_option.default, default)
    vampytest.assert_eq(checkbox_group_option.description, description)
