__all__ = ('ComponentTypeLayoutFlag',)

from datetime import datetime as DateTime, timezone as TimeZone

from scarletio import export

from ...bases import FlagBase, FlagDescriptor as F, FlagDeprecation as FD


@export
class ComponentTypeLayoutFlag(FlagBase):
    """
    Represents a components layout information.
    +---------------------------+-------------------+
    | Respective name           | Bitwise position  |
    +===========================+===================+
    | allowed_in_message        | 0                 |
    +---------------------------+-------------------+
    | allowed_in_form           | 1                 |
    +---------------------------+-------------------+
    | top_level                 | 2                 |
    +---------------------------+-------------------+
    | nestable_into_row         | 3                 |
    +---------------------------+-------------------+
    | nestable_into_container   | 4                 |
    +---------------------------+-------------------+
    | nestable_into_section     | 5                 |
    +---------------------------+-------------------+
    | section_thumbnail         | 6                 |
    +---------------------------+-------------------+
    | version_1                 | 7                 |
    +---------------------------+-------------------+
    | version_2                 | 8                 |
    +---------------------------+-------------------+
    """
    allowed_in_message = F(0)
    allowed_in_form = F(1)
    top_level = F(2)
    nestable_into_row = F(3)
    nestable_into_container = F(4)
    nestable_into_section = F(5)
    section_thumbnail = F(6)
    version_1 = F(7)
    version_2 = F(8)
    
    
    nestable = F(
        nestable_into_row.shift,
        deprecation = FD(
            'nestable_into_row',
            DateTime(2025, 10, 28, tzinfo = TimeZone.utc),
        ),
    )
