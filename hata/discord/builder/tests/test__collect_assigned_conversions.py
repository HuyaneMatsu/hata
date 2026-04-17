import vampytest

from ..builder_base import _collect_assigned_conversions

from .helpers import _create_default_conversion, TestType


def _iter_options():
    conversion_0 = _create_default_conversion()
    
    yield (
        (),
        {},
        {},
    )
    yield (
        (),
        {'mister': conversion_0},
        {'mister': conversion_0},
    )
    yield (
        (
            TestType({'CONVERSIONS_ASSIGNED': {'hey': conversion_0}}),
        ),
        {},
        {'hey': conversion_0},
    )
    yield (
        (
            TestType({'CONVERSIONS_ASSIGNED': {}}),
            TestType({'CONVERSIONS_ASSIGNED': {'hey': conversion_0}}),
            TestType({'CONVERSIONS_ASSIGNED': {}}),
        ),
        {},
        {'hey': conversion_0},
    )
    yield (
        (
            TestType({'CONVERSIONS_ASSIGNED': {'sister': conversion_0}}),
            TestType({'CONVERSIONS_ASSIGNED': {}, 'sister': None}),
        ),
        {},
        {},
    )
    yield (
        (
            TestType({'CONVERSIONS_ASSIGNED': {'hey': conversion_0}}),
        ),
        {'hey': None},
        {},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__collect_assigned_conversions(builder_types, type_attributes):
    """
    Tests whether ``_collect_assigned_conversions`` works as intended.
    
    Parameters
    ----------
    builder_types : `list<type>`
        Inherited builder types to collect from.
    type_attributes : `dict<str, object>`
        The type attributes of the type to be created.
    
    Returns
    -------
    output : `dict<str, Conversion>`
    """
    return _collect_assigned_conversions(builder_types, type_attributes)
