import vampytest

from ...application_entity import ApplicationEntity

from ..fields import put_publishers_into


def test__put_publishers_into():
    """
    Tests whether ``put_publishers_into`` works as intended.
    
    Case: include internals.
    """
    application_entity = ApplicationEntity.precreate(202211270001)
    
    for input_, defaults, expected_output in (
        (None, True, {'publishers': []}),
        (
            [application_entity],
            False,
            {'publishers': [application_entity.to_data(defaults = True, include_internals = True)]}
        ),
    ):
        data = put_publishers_into(input_, {}, defaults, include_internals = True)
        vampytest.assert_eq(data, expected_output)
