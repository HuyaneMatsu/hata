import vampytest

from ...embed_provider import EmbedProvider

from ..fields import put_provider_into


def test__put_provider_into():
    """
    Tests whether ``put_provider_into`` is working as intended.
    """
    provider = EmbedProvider(name = 'hell')
    
    for input_value, defaults, expected_output in (
        (None, False, {}),
        (provider, False, {'provider': provider.to_data()}),
        (provider, True, {'provider': provider.to_data(defaults = True)}),
    ):
        data = put_provider_into(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
