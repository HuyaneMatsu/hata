import vampytest

from ..checkbox_group_option import CheckboxGroupOption

from .test__CheckboxGroupOption__constructor import _assert_fields_set


def test__CheckboxGroupOption__from_data():
    """
    Tests whether ``CheckboxGroupOption.from_data`` works as intended.
    """
    value = 'last'
    label = 'night'
    default = True
    description = 'good'
    
    data = {
        'value': value,
        'label': label,
        'default': default,
        'description': description,
    }
    
    checkbox_group_option = CheckboxGroupOption.from_data(data)
    _assert_fields_set(checkbox_group_option)
    vampytest.assert_eq(checkbox_group_option.value, value)
    vampytest.assert_eq(checkbox_group_option.label, label)
    vampytest.assert_eq(checkbox_group_option.default, default)
    vampytest.assert_eq(checkbox_group_option.description, description)


def test__CheckboxGroupOption__to_data():
    """
    Tests whether ``CheckboxGroupOption.to_data`` works as intended.
    
    Case: include defaults
    """
    value = 'last'
    label = 'night'
    default = True
    description = 'good'
    
    checkbox_group_option = CheckboxGroupOption(value, label, default = default, description = description)
  
    vampytest.assert_eq(
        checkbox_group_option.to_data(
            defaults = True,
        ),
        {
            'value': value,
            'label': label,
            'default': default,
            'description': description,
        },
    )
