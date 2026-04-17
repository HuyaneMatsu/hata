import vampytest

from ..conversions import CONVERSION_CONTENT
from ..message_builder import MessageBuilderBase


def test__MessageBuilderBase__with_positional_parameter_unknown():
    """
    Tests whether ``MessageBuilderBase._with_positional_parameter_unknown`` works as intended.
    """
    value = [12] 
    
    message_builder = MessageBuilderBase()
    message_builder._with_positional_parameter_unknown(value)
    
    vampytest.assert_eq(
        message_builder.fields,
        {
            CONVERSION_CONTENT : str(value),
        },
    )
