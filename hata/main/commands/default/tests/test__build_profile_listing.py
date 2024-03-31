import vampytest

from ..profiling import build_profile_listing


def test__build_profile_listing():
    """
    Tests whether ``build_profile_listing`` works as intended.
    """
    names = ['hey', 'mister']
    output = build_profile_listing(names)
    
    vampytest.assert_instance(output, str)
    vampytest.assert_eq(
        output,
        (
            '- hey\n'
            '- mister\n'
        )
    )
