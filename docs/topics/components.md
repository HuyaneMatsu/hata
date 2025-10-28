# Introduction

Message components, mainly known just as components, are UI elements that can be included with a message.
Your application or bot can send them, allowing the users to see the displayed content and to interact with them.

We can separate components to 3 categories:

- Layout components - Modify how the shown content is structured.
- Content components - Show either text or media.
- Interactive components - Allows the user to interact with them.

Components can be passed to `InteractionResponse` and to many client methods as well:

- `.message_create`
- `.message_edit`
- `.webhook_message_create`
- `.webhook_message_edit`
- `.interaction_response_message_create`
- `.interaction_response_message_edit`
- `.interaction_followup_message_create`
- `.interaction_followup_message_edit`
- `.interaction_component_message_edit`


If you're not interested how to layout components or in their limitations you can skip ahead to either
[content_components](content_components.md) or [interactive components](interactive_components.md).

## Component layouts

Currently there are 3 types of layout components:

- Row - currently the only layout component that allows stacking components horizontally.
    It can contain only interactive components: up to 5 buttons, but only 1 of any other interactive component.
- Container - can contain any other top level component (except itself),
    has a color strip on the left just like embeds.
- Section - can contain only text display components, but allows you to have a thumbnail on the top right
    just like embeds do. The only difference is that the thumbnail can not only be a media, but a button as well.


When passing `components` as a parameter, Hata will try to auto-align them.
As an example, buttons cannot be used as top level components, so they are automatically nested into rows:

```py3
components = [
    create_button(...),
    create_button(...),
    create_button(...),
]

# Equals to:

components = [
    create_row(create_button(...)),
    create_row(create_button(...)),
    create_row(create_button(...)),
]
```

This and a few other conditions allow for a more relaxed experience.

For example, passing a single component:

```py3
components = create_button(...)

# Equals to:

components = [
    create_row(create_button(...)),
]
```

Or nested list row-packing:

```py3
components = [
    [create_button(...), create_button(...), create_button(...)],
]

# Equals to:

components = [
    create_row(create_button(...), create_button(...), create_button(...)),
]
```

## Versioning

Currently components can be separated to 2 versions.

### version 1

They can be attached to any message. See the table [overview](#overview) for supported components.

### version 2

They consist of content components and related layout components.
These content and layout components allow you to structure your message in a more relaxed way.
They cannot be used alongside `embeds` and `content` fields.

If a message contains at least one "version 2" component, it has to be marked as "version 2".
Hata does this for you automatically.

## Limitations

- A message can have up to `5` top level components if v1, there is no such a limit in v2.
- `custom_id` can be `100` character long.
- A message can have up to `40` total components.
- The displayable content cannot exceed `4000` characters.
    This excludes the text on interactive components and media descriptions.

### Button limitations

- Up to `5` buttons can be in a row.
- Component `label` can be `80` characters long.

### Select limitations

- Up to `1` select can be in a row.
- A select can have `25` choices.
- A select can have choices in range `[1:25]`.
- Select `min_values` can be in range `[0:15]`.
- Select `max_values` can be in range `[1:25]`.


## Overview

Here is a complete overview of where components can be used, how can they be nested and much more.


| Component type name | Allowed in message | Allowed in form | Top level | Nestable into row | Nestable into container | Nestable into section | Nestable into label    | Section thumbnail | Holds value single    | Holds value multiple  | Version 1 | Version 2 |
|---------------------|--------------------|-----------------|-----------|-------------------|-------------------------|-----------------------|------------------------|-------------------|-----------------------|-----------------------|-----------|-----------|
| none                |                    |                 |           |                   |                         |                       |                        |                   |                       |                       |           |           |
| row                 | X                  | X               | X         |                   | X                       |                       |                        |                   |                       |                       | X         |           |
| button              | X                  |                 |           | X                 |                         |                       |                        | X                 |                       |                       | X         |           |
| string select       | X                  | X               |           | X                 |                         |                       | X                      |                   |                       | X                     | X         |           |
| text input          |                    | X               |           | X                 |                         |                       | X                      |                   | X                     |                       | X         |           |
| user select         | X                  | X               |           | X                 |                         |                       | X                      |                   |                       | X                     | X         |           |
| role select         | X                  | X               |           | X                 |                         |                       | X                      |                   |                       | X                     | X         |           |
| mentionable select  | X                  | X               |           | X                 |                         |                       | X                      |                   |                       | X                     | X         |           |
| channel select      | X                  | X               |           | X                 |                         |                       | X                      |                   |                       | X                     | X         |           |
| section             | X                  |                 | X         |                   | X                       |                       |                        |                   |                       |                       |           | X         |
| text display        | X                  | X               | X         |                   | X                       | X                     |                        |                   |                       |                       |           | X         |
| thumbnail media     | X                  |                 |           |                   |                         |                       |                        | X                 |                       |                       |           | X         |
| media gallery       | X                  |                 | X         |                   | X                       |                       |                        |                   |                       |                       |           | X         |
| attachment media    | X                  |                 | X         |                   | X                       |                       |                        |                   |                       |                       |           | X         |
| separator           | X                  |                 | X         |                   | X                       |                       |                        |                   |                       |                       |           | X         |
| container           | X                  |                 | X         |                   |                         |                       |                        |                   |                       |                       |           | X         |
| label               |                    | X               | X         |                   |                         |                       |                        |                   |                       |                       |           | X         |
| attachment input    |                    | X               |           |                   |                         |                       | X                      |                   |                       | X                     |           | X         |


This information can also be accessed at runtime:

```py3
In [0]: print(ComponentType.container.layout_flags.top_level)
True
In [1]: print(ComponentType.container.layout_flags.allowed_in_form)
False
```

----

<p align="left">
    <a href="./auto_completion.md">Previously: Auto completion</a>
</p>

<p align="right">
    <a href="./content_components.md">Next up: Content components</a>
</p>
