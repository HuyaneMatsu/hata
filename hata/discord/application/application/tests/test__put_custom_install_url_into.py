import vampytest

from ..fields import put_custom_install_url_into


def test__put_custom_install_url_into():
    """
    Tests whether ``put_custom_install_url_into`` is working as intended.
    """
    for input_, defaults, expected_output in (
        (None, False, {}),
        ('https://orindance.party/', False, {'custom_install_url': 'https://orindance.party/'}),
    ):
        data = put_custom_install_url_into(input_, {}, defaults)
        vampytest.assert_eq(data, expected_output)
