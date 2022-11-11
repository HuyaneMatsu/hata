import vampytest

from ..fields import put_options_into
from ..interaction_option import InteractionOption


def test__put_options_into():
    """
    Tests whether ``put_options_into`` is working as intended.
    """
    option = InteractionOption(name = 'overkill')
    
    for input_, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'options': []}),
        ((option, ), False, {'options': [option.to_data()]}),
    ):
        data = put_options_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
