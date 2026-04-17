import vampytest

from ..component import Component, ComponentType
from ..media_info import MediaInfo
from ..utils import create_attachment_media


def test__create_attachment_media():
    """
    Tests whether ``create_attachment_media`` works as intended.
    """
    media = MediaInfo('attachment://big_braids_orin.png')
    spoiler = True
    
    component = create_attachment_media(
        media,
        spoiler = spoiler,
    )
    
    vampytest.assert_instance(component, Component)
    vampytest.assert_is(component.type, ComponentType.attachment_media)
    vampytest.assert_eq(component.media, media)
    vampytest.assert_is(component.spoiler, spoiler)
