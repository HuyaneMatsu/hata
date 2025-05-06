# Introduction

Using content with layout components allow you to structure your message in a more relaxed way than regular `content`,
`embeds` and `attachments`, although they are mutually exclusive with the `embeds` and `content` fields.

This guide consists of less commands than the others ones, instead focusing on usage, introducing components one by one.


## Text Display

Text display components currently are the only one components that can display text.
Their functionality equals to regular `content`, but they can be used in an un-ordered manner compared to it.

```py3
components = [
    create_text_display('# Kawashiro Nitori'),
    create_text_display(
        'I am a shy kappa who lives in Genbu Ravine next to the Youkai Mountain. '
        'I have the power to control water, I am specializing in engineering and technology.'
    ),
    create_text_display('# *Runs away*'),
]

```

These components support mentions and markdowns as normal message content.
Additionally you can create a small spacing between them (around the size of half line break) by using multiple after
each other.

## Separator

Speaking of the spacing! There is a separate separator component, that allows you to set how big the separator space
should be and whether there should be a divider.


```py3
components = [
    create_text_display('# Kawashiro Nitori'),
    create_separator(),
    create_text_display(
        'I am a shy kappa who lives in Genbu Ravine next to the Youkai Mountain. '
        'I have the power to control water, I am specializing in engineering and technology.'
    ),
    create_text_display('# *Runs away*'),
]
```

By default separators will have a divider and the spacing size will be small (around the size of one line break).
This should cover most common use case.

The divider can be removed and the spacing can be increased to large (around the size of one and half line breaks). 

```py3
create_separator(divider = False, spacing_size = SeparatorSpacingSize.large),
```

### Section

Text display components can be grouped into sections. These sections allow you to set a thumbnail, that is just like
at the case of embeds, an image, but it can also be a button.

```py3
components = [
    create_text_display('# Kawashiro Nitori'),
    create_separator(),
    create_section(
        create_text_display(
            'I am a shy kappa who lives in Genbu Ravine next to the Youkai Mountain. '
            'I have the power to control water, I am specializing in engineering and technology.'
        ),
        thumbnail = create_thumbnail_media(url),
    ),
    create_section(
        create_text_display('-# *Runs away*'),
        thumbnail = create_button('Follow', custom_id = 'nitori_info.follow'),
    ),
]
```

By stacking sections with thumbnail after each other you can create something unexpectedly charming.

Thumbnails can have an alternative description and set to be spoilered. 

```py3
create_thumbnail_media(url, description = 'Kawashiro Nitori', spoiler = True)
```

## Media Gallery

There is a component just for displaying the previews of various medias that include both images and shockingly
videos as well.
One to ten medias can be used in a single media gallery. 

```py3
url = 'https://en.touhouwiki.net/images/7/70/Th185Nitori.png'

components = [
    create_text_display('# Kawashiro Nitori'),
    create_separator(),
    create_section(
        create_text_display(
            'I am a shy kappa who lives in Genbu Ravine next to the Youkai Mountain. '
            'I have the power to control water, I am specializing in engineering and technology.'
        ),
        thumbnail = create_thumbnail_media(url),
    ),
    create_section(
        create_text_display('-# *Runs away*'),
        thumbnail = create_button('Follow', custom_id = 'nitori_info.follow'),
    ),
    create_separator(divider = False, spacing_size = SeparatorSpacingSize.large),
    create_text_display('Additional images:'),
    create_media_gallery(url, url, url),
]
```

Their layout currently cannot be customized, but since they are displayed the exact same way as image attachment
previews of regular messages they are not specially hard to figure out.

By using `MediaGalleryItem`-s you can assign additional alternative description to each media and also make them
spoilered.

```py3
create_media_gallery(
    MediaGalleryItem(url, description = 'Kawashiro Nitori sitting', spoiler = True),
    MediaGalleryItem(url, description = 'Kawashiro Nitori looking', spoiler = True),
    MediaGalleryItem(url, description = 'Kawashiro Nitori at table', spoiler = True),
)
```

## Attachment media

With attachment media you can display a single attachment without preview.

```py3
url = 'https://en.touhouwiki.net/images/7/70/Th185Nitori.png'

components = [
    create_text_display('# Kawashiro Nitori'),
    create_separator(),
    create_section(
        create_text_display(
            'I am a shy kappa who lives in Genbu Ravine next to the Youkai Mountain. '
            'I have the power to control water, I am specializing in engineering and technology.'
        ),
        thumbnail = create_thumbnail_media(url),
    ),
    create_section(
        create_text_display('-# *Runs away*'),
        thumbnail = create_button('Follow', custom_id = 'nitori_info.follow'),
    ),
    create_separator(divider = False, spacing_size = SeparatorSpacingSize.large),
    create_text_display('My cv:'),
    create_attachment_media('attachment://cv.txt'),
    create_separator(divider = False, spacing_size = SeparatorSpacingSize.large),
    create_text_display('Reference images:'),
    create_media_gallery(url, url, url),
]
```

Attachment media only allows you to use the `attachment://<file_name>` protocol.

You can additional mark attachments as spoilered.

```py3
create_attachment_media('attachment://cv.txt', spoiler = True)
```

## Container

You can have visibly distinct groups of components by using containers.
They allow putting under them any other top level component.
You can also use the `color` parameter to have them a colored strip on the left side, just like at the case of embeds.


```py3
url = 'https://en.touhouwiki.net/images/7/70/Th185Nitori.png'

components = [
    create_container(
        create_text_display('# Kawashiro Nitori'),
        create_separator(),
        create_section(
            create_text_display(
                'I am a shy kappa who lives in Genbu Ravine next to the Youkai Mountain. '
                'I have the power to control water, I am specializing in engineering and technology.'
            ),
            thumbnail = create_thumbnail_media(url),
        ),
        create_section(
            create_text_display('-# *Runs away*'),
            thumbnail = create_button('Follow', custom_id = 'nitori_info.follow'),
        ),
        create_separator(divider = False, spacing_size = SeparatorSpacingSize.large),
        create_text_display('my cv:'),
        create_attachment_media('attachment://cv.txt'),
        create_separator(divider = False, spacing_size = SeparatorSpacingSize.large),
        create_text_display('Reference images:'),
        create_media_gallery(url, url, url),
        create_row(
            create_button('Hug them (dangerous)', custom_id = 'nitori_info.hug'),
            create_button('Pat them (dangerous)', custom_id = 'nitori_info.pat'),
            create_button('Ignore them (certain death)', custom_id = 'nitori_info.ignore'),
        ),
        color = Color.from_rgb(0, 0, 255),
    ),
]
```

You can also spoiler whole containers.

```py3
create_container(
    create_media_gallery(url, url, url),
    spoiler = True,
)

```

# Putting it together

Lets put a full command together from the above components.

Since showcased a few buttons in the examples to show that [interactive components](interactive_components.md),
can also be used within layout components, also adding basic handing for them.

```py3
from hata import (
    Color, SeparatorSpacingSize, create_attachment_media, create_button, create_container, create_media_gallery,
    create_row, create_section, create_separator, create_text_display, create_thumbnail_media
)
from hata.ext.slash import InteractionResponse


NITORI_IMAGE_URL = 'https://en.touhouwiki.net/images/7/70/Th185Nitori.png'
NITORI_CV = '*mechanical arm blue print*'
NITORI_COLOR = Color.from_rgb(0, 0, 255)

NITORI_CUSTOM_ID_BASE = 'nitori_info'
NITORI_CUSTOM_ID_FOLLOW = f'{NITORI_CUSTOM_ID_BASE}.follow'
NITORI_CUSTOM_ID_HUG = f'{NITORI_CUSTOM_ID_BASE}.hug'
NITORI_CUSTOM_ID_PAT = f'{NITORI_CUSTOM_ID_BASE}.pat'
NITORI_CUSTOM_ID_IGNORE = f'{NITORI_CUSTOM_ID_BASE}.ignore'


@Nitori.interactions(guild = TEST_GUILD)
async def nitori_info():
    """Information about Kawashiro Nitori."""
    return InteractionResponse(
        attachments = [
            ('cv.txt', NITORI_CV),
        ],
        components = [
            create_container(
                create_text_display('# Kawashiro Nitori'),
                create_separator(),
                create_section(
                    create_text_display(
                        'I am a shy kappa who lives in Genbu Ravine next to the Youkai Mountain. '
                        'I have the power to control water, I am specializing in engineering and technology.'
                    ),
                    thumbnail = create_thumbnail_media(NITORI_IMAGE_URL),
                ),
                create_section(
                    create_text_display('-# *Runs away*'),
                    thumbnail = create_button('Follow', custom_id = NITORI_CUSTOM_ID_FOLLOW),
                ),
                create_separator(divider = False, spacing_size = SeparatorSpacingSize.large),
                create_text_display('my cv:'),
                create_attachment_media('attachment://cv.txt'),
                create_separator(divider = False, spacing_size = SeparatorSpacingSize.large),
                create_text_display('Reference images:'),
                create_media_gallery(NITORI_IMAGE_URL, NITORI_IMAGE_URL, NITORI_IMAGE_URL),
                create_row(
                    create_button('Hug them (dangerous)', custom_id = NITORI_CUSTOM_ID_HUG),
                    create_button('Pat them (dangerous)', custom_id = NITORI_CUSTOM_ID_PAT),
                    create_button('Ignore them (certain death)', custom_id = NITORI_CUSTOM_ID_IGNORE),
                ),
                color = NITORI_COLOR,
            ),
        ],
    )


@Nitori.interactions(
    custom_id = [
        NITORI_CUSTOM_ID_FOLLOW,
        NITORI_CUSTOM_ID_HUG,
        NITORI_CUSTOM_ID_PAT,
        NITORI_CUSTOM_ID_IGNORE,
    ],
)
async def nitori_action(client, event):
    await client.interaction_component_acknowledge(event)
    await client.interaction_followup_message_create(event, 'You died')
```

The long awaited output:

![](assets/content_components_0000.png)

----

<p align="left">
    <a href="./components.md">Previously: Components</a>
</p>

<p align="right">
    <a href="./interactive_components.md">Next up: Interactive components</a>
</p>
