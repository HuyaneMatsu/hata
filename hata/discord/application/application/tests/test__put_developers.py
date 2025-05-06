import vampytest

from ...application_entity import ApplicationEntity

from ..fields import put_developers


def test__put_developers():
    """
    Tests whether ``put_developers`` works as intended.
    
    Case: include internals.
    """
    application_entity = ApplicationEntity.precreate(202211270001)
    
    for input_, defaults, expected_output in (
        (None, True, {'developers': []}),
        (
            [application_entity],
            False,
            {'developers': [application_entity.to_data(defaults = True, include_internals = True)]}
        ),
    ):
        data = put_developers(input_, {}, defaults, include_internals = True)
        vampytest.assert_eq(data, expected_output)
