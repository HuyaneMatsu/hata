import vampytest

from ..fields import put_options
from ..interaction_option import InteractionOption


def test__put_options():
    """
    Tests whether ``put_options`` is working as intended.
    """
    option = InteractionOption(name = 'overkill')
    
    for input_, defaults, expected_output in (
        (None, False, {}),
        (None, True, {'options': []}),
        ((option, ), False, {'options': [option.to_data()]}),
    ):
        data = put_options(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
