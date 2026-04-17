import vampytest

from ..component import Component, ComponentType
from ..media_info import MediaInfo
from ..utils import create_thumbnail_media


def test__create_thumbnail_media():
    """
    Tests whether ``create_thumbnail_media`` works as intended.
    """
    description = 'Its Orin <3'
    media = MediaInfo('thumbnail://big_braids_orin.png')
    spoiler = True
    
    component = create_thumbnail_media(
        media,
        description = description,
        spoiler = spoiler,
    )
    
    vampytest.assert_instance(component, Component)
    vampytest.assert_is(component.type, ComponentType.thumbnail_media)
    vampytest.assert_eq(component.description, description)
    vampytest.assert_eq(component.media, media)
    vampytest.assert_is(component.spoiler, spoiler)
