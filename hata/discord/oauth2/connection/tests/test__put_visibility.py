import vampytest

from ..preinstanced import ConnectionVisibility

from ..fields import put_visibility


def test__put_visibility():
    """
    Tests whether ``put_visibility`` is working as intended.
    """
    for input_value, defaults, expected_output in (
        (ConnectionVisibility.user_only, False, {}),
        (ConnectionVisibility.everyone, False, {'visibility': ConnectionVisibility.everyone.value}),
        (ConnectionVisibility.user_only, True, {'visibility': ConnectionVisibility.user_only.value}),
    ):
        data = put_visibility(input_value, {}, defaults)
        vampytest.assert_eq(data, expected_output)
