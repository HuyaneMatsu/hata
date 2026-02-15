import vampytest

from ..radio_group_option import RadioGroupOption

from .test__RadioGroupOption__constructor import _assert_fields_set


def test__RadioGroupOption__from_data():
    """
    Tests whether ``RadioGroupOption.from_data`` works as intended.
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
    
    radio_group_option = RadioGroupOption.from_data(data)
    _assert_fields_set(radio_group_option)
    vampytest.assert_eq(radio_group_option.value, value)
    vampytest.assert_eq(radio_group_option.label, label)
    vampytest.assert_eq(radio_group_option.default, default)
    vampytest.assert_eq(radio_group_option.description, description)


def test__RadioGroupOption__to_data():
    """
    Tests whether ``RadioGroupOption.to_data`` works as intended.
    
    Case: include defaults
    """
    value = 'last'
    label = 'night'
    default = True
    description = 'good'
    
    radio_group_option = RadioGroupOption(value, label, default = default, description = description)
  
    vampytest.assert_eq(
        radio_group_option.to_data(
            defaults = True,
        ),
        {
            'value': value,
            'label': label,
            'default': default,
            'description': description,
        },
    )
